import os
import shutil
import sys
import datetime
from datetime import timezone, timedelta
import json
import hashlib
import re
import random
from pathlib import Path
from multiprocessing import Pool, cpu_count

# --- Core Helper Functions ---

def get_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def run_shell_cmd(command, cwd=None, shell=True):
    import subprocess
    try:
        result = subprocess.run(command, cwd=cwd, shell=shell, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}\n{e.stderr}")
        return ""

def calculate_year_progress(use_utc8=False):
    if use_utc8:
        now = datetime.datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None)
    else:
        now = datetime.datetime.now()
    current_time = now.strftime("%Y年%m月%d日")
    year_start = datetime.datetime(now.year, 1, 1)
    year_end = datetime.datetime(now.year, 12, 31)
    days_total = (year_end - year_start).days + 1
    days_passed = (now - year_start).days + 1
    return current_time, round((days_passed / days_total) * 100, 1), days_total - days_passed

def calculate_progress_for_date(date_str, use_utc8=False):
    try:
        dt = datetime.datetime.strptime(date_str, "%Y年%m月%d日")
    except ValueError:
        try:
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return calculate_year_progress(use_utc8)
    year_start = datetime.datetime(dt.year, 1, 1)
    year_end = datetime.datetime(dt.year, 12, 31)
    days_total = (year_end - year_start).days + 1
    days_passed = (dt - year_start).days + 1
    return dt.strftime("%Y年%m月%d日"), round((days_passed / days_total) * 100, 1), days_total - days_passed

# --- Parallel Worker ---

def process_single_file(args):
    md_file_str, md_dir_str, cache_entry, global_current_time, img_base_url, use_utc8 = args
    md_file = Path(md_file_str)
    MD_DIR = Path(md_dir_str)
    import markdown2
    
    file_hash = get_file_hash(md_file)
    if cache_entry and cache_entry.get('hash') == file_hash:
        return cache_entry['data'], False

    rel_path_from_md = md_file.relative_to(MD_DIR)
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        sys_mtime = os.path.getmtime(md_file)
        if use_utc8:
            dt_sys = datetime.datetime.fromtimestamp(sys_mtime, timezone(timedelta(hours=8))).replace(tzinfo=None)
        else:
            dt_sys = datetime.datetime.fromtimestamp(sys_mtime)
        sys_date_str = dt_sys.strftime("%Y-%m-%d %H:%M:%S")
        updated_match = re.search(r'^updated:\s*(\d{4}-\d{2}-\d{2}(?: \d{2}:\d{2}:\d{2})?)', content, re.MULTILINE)
        sort_date = updated_match.group(1) if updated_match else sys_date_str
        if len(sort_date) == 10: sort_date += " 00:00:00"
    except Exception: sort_date = "0000-00-00 00:00:00"

    title = md_file.stem
    article_date = None
    fm_pattern = r'^---\s*\r?\n(.*?)\r?\n---\s*\r?\n'
    fm_match = re.match(fm_pattern, content, re.DOTALL)
    if fm_match:
        fm_content = fm_match.group(1)
        content_body = content[fm_match.end():]
        for line in fm_content.split('\n'):
            line = line.strip()
            if line.startswith('title:'): title = line.replace('title:', '').strip()
            elif line.startswith('date:'):
                article_date = line.replace('date:', '').strip()
                if re.match(r'\d{4}-\d{2}-\d{2}', article_date):
                    parts = article_date.split(' ')[0].split('-')
                    article_date = f"{parts[0]}年{parts[1]}月{parts[2]}日"
    else:
        fn_match = re.search(r'(\d{4})[年\-](\d{2})[月\-](\d{2})日?', md_file.name)
        article_date = f"{fn_match.group(1)}年{fn_match.group(2)}月{fn_match.group(3)}日" if fn_match else global_current_time
        content_body = content

    art_time_str, art_progress, art_days_rem = calculate_progress_for_date(article_date, use_utc8)
    
    # Image Paths Fix: Move manipulation out of f-string for Python < 3.12 compatibility
    def fix_md_img(match):
        alt, src = match.group(1), match.group(2)
        if src.startswith(('http://', 'https://')): return match.group(0)
        filename = src.replace("\\", "/").split("/")[-1]
        return f"![{alt}]({img_base_url}/{filename})"

    def fix_html_img(match):
        tag, src = match.group(0), match.group(1)
        if src.startswith(('http://', 'https://')): return tag
        filename = src.replace("\\", "/").split("/")[-1]
        return tag.replace(src, f"{img_base_url}/{filename}")

    content_body = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', fix_md_img, content_body)
    content_body = re.sub(r'<img[^>]+src="([^"]+)"', fix_html_img, content_body)

    html_content = markdown2.markdown(content_body, extras=["fenced-code-blocks", "tables"])
    text_content = re.sub(r'<[^>]+>', '', html_content.replace('<p>', '').replace('</p>', ' ').replace('\n', ' '))
    truncated = text_content[:200] + "..." if len(text_content) > 200 else text_content
    img_match = re.search(r'<img[^>]+src="([^">]+)"', html_content)
    thumbnail = img_match.group(1) if img_match else None

    display_updated = ""
    try:
        display_updated = datetime.datetime.strptime(sort_date, "%Y-%m-%d %H:%M:%S").strftime("%Y年%m月%d日 %H:%M")
    except Exception: display_updated = sort_date

    # Breadcrumbs Logic
    path_parts = list(rel_path_from_md.parent.parts)
    breadcrumbs = [{"name": "首页", "url": "/index.html"}]
    current_p = ""
    for part in path_parts:
        if part and part != '.':
            current_p = os.path.join(current_p, part)
            slug = current_p.replace(os.sep, '_')
            breadcrumbs.append({"name": part, "url": f"/{slug}.html"})

    return {
        "title": title, "md_file_rel": str(rel_path_from_md), "truncated_content": truncated,
        "full_content": html_content, "date": article_date, "updated": display_updated,
        "sort_date": sort_date, "art_time_str": art_time_str, "art_progress": art_progress,
        "art_days_rem": art_days_rem, "thumbnail": thumbnail, "type": "file", "hash": file_hash,
        "breadcrumbs": breadcrumbs
    }, True

# --- Main Engine ---

class SiteGenerator:
    def __init__(self, config):
        self.config = config
        self.base_dir = Path(config['BASE_DIR'])
        self.public_dir = self.base_dir / config['PUBLIC_DIR_NAME']
        self.cache_file = self.base_dir / config['CACHE_FILE_NAME']
        self.md_dir = Path(config['MD_DIR'])
        if not self.md_dir.exists():
            self.md_dir = Path(config['MD_DIR_FALLBACK'])

    def generate(self):
        print(f"\n🚀 Generating Site: {self.config['SITE_NAME']}...")
        from jinja2 import Environment, FileSystemLoader
        import markdown2

        # 1. Load Cache
        cache_data = {}
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f: cache_data = json.load(f)
            except Exception: pass

        # 2. Setup Directories
        if self.public_dir.exists(): shutil.rmtree(self.public_dir, onerror=on_rm_error)
        self.public_dir.mkdir(parents=True, exist_ok=True)
        static_src = self.base_dir / 'static'
        if static_src.exists(): shutil.copytree(static_src, self.public_dir / 'static')

        # 3. Time Info
        global_current_time, global_year_progress, global_days_remaining = calculate_year_progress(self.config.get('USE_UTC8', False))

        # 4. Parallel Processing Articles
        md_files = [f for f in self.md_dir.rglob('*.md') if f.name.lower() != 'about.md']
        print(f"  Processing {len(md_files)} files...")

        worker_args = [(str(f), str(self.md_dir), cache_data.get(str(f.relative_to(self.md_dir))), 
                        global_current_time, self.config['IMG_BASE_URL'], self.config.get('USE_UTC8', False)) for f in md_files]
        
        with Pool(processes=cpu_count()) as pool:
            results = pool.map(process_single_file, worker_args)

        files, new_cache = [], {}
        modified_count = 0
        for res, modified in results:
            files.append(res)
            new_cache[res['md_file_rel']] = {'hash': res['hash'], 'data': res}
            if modified: modified_count += 1
        print(f"  Done. {modified_count} processed, {len(files)-modified_count} cached.")

        with open(self.cache_file, 'w', encoding='utf-8') as f: json.dump(new_cache, f, ensure_ascii=False)

        # 5. Sorting & Paths
        files.sort(key=lambda x: x['sort_date'], reverse=True)
        date_tracker = {}
        for f in files:
            d_m = re.search(r'(\d{4})[年\-](\d{2})[月\-](\d{2})', f['date'])
            b_id = f"{d_m.group(1)}{d_m.group(2)}{d_m.group(3)}" if d_m else f['sort_date'][:10].replace('-', '')
            if b_id not in date_tracker: date_tracker[b_id] = 0; f['rel_path'] = f"{b_id}.html"
            else: date_tracker[b_id] += 1; f['rel_path'] = f"{b_id}-{date_tracker[b_id]}.html"
            f['output_path'] = self.public_dir / f['rel_path']

        # 6. Build Directory Tree
        directory_tree = {}
        top_node = self.config.get('TREE_TOP_NODE')
        if top_node:
            directory_tree[top_node] = {'type': 'directory', 'expanded': True, 'count': 0, 'children': {}}
            root_curr = directory_tree[top_node]['children']
        else:
            root_curr = directory_tree

        for f in files:
            if 'aoao推荐' in Path(f['md_file_rel']).parts: continue
            curr = root_curr
            parts = Path(f['md_file_rel']).parts
            for i, part in enumerate(parts):
                if i == len(parts)-1: curr[f['title']] = f
                else:
                    if part not in curr or curr[part].get('type') != 'directory':
                        curr[part] = {'type': 'directory', 'expanded': False, 'count': 0, 'children': {}}
                    curr = curr[part]['children']

        def sort_count(node):
            l_date, count = "0000-00-00 00:00:00", 0
            for name, item in node.items():
                if item['type'] == 'file':
                    if item['sort_date'] > l_date: l_date = item['sort_date']
                    count += 1
                else:
                    dl, dc = sort_count(item['children'])
                    item['latest_date'], item['count'], count = dl, dc, count + dc
                    if dl > l_date: l_date = dl
            sorted_items = sorted(node.items(), key=lambda x: x[1]['sort_date'] if x[1]['type']=='file' else x[1].get('latest_date', "0000"), reverse=True)
            node.clear()
            for k, v in sorted_items: node[k] = v
            return l_date, count

        sort_count(directory_tree)

        # 7. Recommendations & Related Articles
        recommendations_map = {}
        for f in files:
            if f['md_file_rel'].startswith('aoao推荐'):
                if f['title'] not in recommendations_map: recommendations_map[f['title']] = f
        recommendations = sorted(recommendations_map.values(), key=lambda x: x['sort_date'], reverse=True)

        for f in files:
            p_dir = str(Path(f['md_file_rel']).parent)
            related = [x for x in files if str(Path(x['md_file_rel']).parent) == p_dir and x['title'] != f['title']]
            f['related_articles'] = related[:3]

        # 8. Render Pages
        env = Environment(loader=FileSystemLoader(self.base_dir / 'templates'))
        base_template = env.get_template("base.html")
        index_template = env.get_template("index.html")
        
        for i, f in enumerate(files):
            f['output_path'].parent.mkdir(parents=True, exist_ok=True)
            u_iso = f['sort_date'].replace(' ', 'T') + "+08:00" if f['sort_date'] else ""
            active_path = list(Path(f['md_file_rel']).parent.parts)

            html = base_template.render(
                title=f['title'], site_name=self.config['SITE_NAME'], site_domain=self.config['CNAME'], 
                rel_path=f['rel_path'], content=f['full_content'], meta_description=f['truncated_content'],
                og_image=f['thumbnail'], sort_date=f['sort_date'].split(' ')[0], updated_iso=u_iso,
                current_time=f['art_time_str'], article_updated=f['updated'],
                year_progress=f['art_progress'], days_remaining=f['art_days_rem'],
                prev_page=files[i-1]['rel_path'] if i > 0 else "",
                next_page=files[i+1]['rel_path'] if i < len(files)-1 else "",
                directory_tree=directory_tree,
                related_articles=f['related_articles'],
                breadcrumbs=f.get('breadcrumbs', []),
                active_path=active_path
            )
            with open(f['output_path'], 'w', encoding='utf-8') as out: out.write(html)

        # 9. Category Landing Pages
        print("  Generating Category Landing Pages...")
        category_articles = {}
        for f in files:
            if 'aoao推荐' in Path(f['md_file_rel']).parts: continue
            path_parts = Path(f['md_file_rel']).parent.parts
            current_p = ""
            for part in path_parts:
                if not part or part == '.': continue
                current_p = os.path.join(current_p, part)
                slug = current_p.replace(os.sep, '_')
                if slug not in category_articles:
                    category_articles[slug] = {"name": part, "articles": [], "path_parts": list(current_p.split(os.sep))}
                category_articles[slug]["articles"].append(f)

        for slug, data in category_articles.items():
            out_p = self.public_dir / f"{slug}.html"
            cat_breadcrumbs = [{"name": "首页", "url": "/index.html"}]
            curr_build_p = ""
            for i, p_part in enumerate(data['path_parts']):
                curr_build_p = os.path.join(curr_build_p, p_part)
                c_slug = curr_build_p.replace(os.sep, '_')
                is_last = (i == len(data['path_parts']) - 1)
                cat_breadcrumbs.append({"name": p_part, "url": None if is_last else f"/{c_slug}.html"})

            html = index_template.render(
                files=data['articles'], all_files=[], site_name=f"{data['name']} - {self.config['SITE_NAME']}",
                directory_tree=directory_tree, recommendations=recommendations,
                current_time=global_current_time, year_progress=global_year_progress, days_remaining=global_days_remaining,
                has_prev_page=False, has_next_page=False, page=1, total_pages=1,
                breadcrumbs=cat_breadcrumbs,
                active_path=data['path_parts']
            )
            with open(out_p, 'w', encoding='utf-8') as out: out.write(html)

        # 10. Index Pages
        total_pages = (len(files) + 9) // 10
        for p in range(1, total_pages + 1):
            page_files = files[(p-1)*10 : p*10]
            html = index_template.render(
                files=page_files, all_files=[], site_name=self.config['SITE_NAME'], directory_tree=directory_tree,
                recommendations=recommendations,
                current_time=global_current_time, year_progress=global_year_progress, days_remaining=global_days_remaining,
                has_prev_page=p > 1, has_next_page=p < total_pages, prev_page_number=p-1, next_page_number=p+1, page=p, total_pages=total_pages,
                active_path=[]
            )
            with open(self.public_dir / ('index.html' if p==1 else f'index_{p}.html'), 'w', encoding='utf-8') as out: out.write(html)

        # 11. Search Index & Final Assets
        search_data = [{"title": f['title'], "rel_path": f['rel_path'], "date": f['date'], "truncated_content": f['truncated_content']} for f in files]
        with open(self.public_dir / 'search_index.json', 'w', encoding='utf-8') as f_idx: json.dump(search_data, f_idx, ensure_ascii=False)
        with open(self.public_dir / 'CNAME', 'w') as f_cn: f_cn.write(self.config['CNAME'])
        
        # About Page
        print("  Generating About Page...")
        about_content = ""
        about_md_path = self.md_dir / 'about.md'
        if about_md_path.exists():
            try:
                with open(about_md_path, 'r', encoding='utf-8') as fab:
                    raw_about = fab.read()
                    raw_about = re.sub(r'^---\s*\r?\n.*?\r?\n---\s*\r?\n', '', raw_about, flags=re.DOTALL)
                    about_content = markdown2.markdown(raw_about, extras=["fenced-code-blocks", "tables"])
            except Exception: pass
        
        about_html = env.get_template("about.html").render(
            directory_tree=directory_tree, site_name=self.config['SITE_NAME'],
            current_time=global_current_time, year_progress=global_year_progress, days_remaining=global_days_remaining,
            about_content=about_content,
            active_path=[]
        )
        with open(self.public_dir / 'about.html', 'w', encoding='utf-8') as f_ab: f_ab.write(about_html)

        if (self.base_dir / 'templates' / 'clocklife.html').exists():
            shutil.copy(self.base_dir / 'templates' / 'clocklife.html', self.public_dir / 'clocklife.html')

        print("  Generation complete.")

    def deploy(self):
        print(f"\n🚀 Deploying to {self.config['REPO_URL']}...")
        if not self.public_dir.exists(): return
        run_shell_cmd("git init && git add . && git commit -m 'Deploy via Unified Engine' || true", cwd=self.public_dir)
        deploy_branch = self.config.get('DEPLOY_BRANCH', 'main')
        run_shell_cmd(f"git push -f {self.config['REPO_URL']} master:{deploy_branch}", cwd=self.public_dir)
