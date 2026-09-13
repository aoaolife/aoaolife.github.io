import sys
from pathlib import Path
from generator_core import SiteGenerator

BASE_DIR = Path(__file__).parent.absolute()

CONFIG_EMUSK = {
    'BASE_DIR': str(BASE_DIR),
    'PUBLIC_DIR_NAME': 'public',
    'CACHE_FILE_NAME': '.build_cache.json',
    'MD_DIR': '/mnt/c/aoaolife/马斯克中文日记',
    'MD_DIR_FALLBACK': 'C:/aoaolife/马斯克中文日记',
    'SITE_NAME': '马斯克中文日记',
    'CNAME': 'emusk.cn',
    'SITE_URL': 'https://emusk.cn',
    'REPO_URL': 'git@github.com:aoaolife/emusk.github.io.git',
    'DEPLOY_BRANCH': 'gh-pages',
    'IMG_BASE_URL': 'https://img.aoao.life',
    'USE_UTC8': False,
    'TREE_TOP_NODE': "马斯克中文日记"
}

def sync_content():
    key_file = BASE_DIR / "jiegeedukg.pem"
    if not key_file.exists(): return
    import subprocess
    try: subprocess.run([sys.executable, str(BASE_DIR / "sync_data.py")], check=True, cwd=str(BASE_DIR))
    except Exception: pass

def main():
    gen = SiteGenerator(CONFIG_EMUSK)
    action = sys.argv[1] if len(sys.argv) > 1 else "all"

    if action == "generate": gen.generate()
    elif action == "deploy": gen.deploy()
    elif action == "sync": sync_content()
    elif action == "all":
        sync_content()
        gen.generate()
        gen.deploy()

if __name__ == "__main__":
    main()
