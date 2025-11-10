// static/search.js - 搜索功能实现

(function() {
    const searchBox = document.getElementById('searchBox');
    const searchResults = document.getElementById('searchResults');
    let searchTimeout;

    if (!searchBox || !searchResults) return;

    // 搜索函数
    function performSearch(query) {
        if (!query || query.trim().length < 2) {
            searchResults.style.display = 'none';
            searchResults.innerHTML = '';
            return;
        }

        query = query.trim().toLowerCase();
        const results = [];

        // 搜索所有文章
        if (window.allArticles && Array.isArray(window.allArticles)) {
            window.allArticles.forEach(article => {
                const title = (article.title || '').toLowerCase();
                const content = stripHtml(article.content || '').toLowerCase();
                const truncated = stripHtml(article.truncated_content || '').toLowerCase();
                
                // 检查标题和内容是否匹配
                const titleMatch = title.includes(query);
                const contentMatch = content.includes(query) || truncated.includes(query);
                
                if (titleMatch || contentMatch) {
                    // 计算相关性分数
                    let score = 0;
                    if (titleMatch) score += 10;
                    if (contentMatch) score += 5;
                    
                    // 获取匹配的上下文
                    const excerpt = getExcerpt(content || truncated, query, 150);
                    
                    results.push({
                        title: article.title,
                        path: article.rel_path,
                        excerpt: excerpt,
                        score: score
                    });
                }
            });
        }

        // 按相关性排序
        results.sort((a, b) => b.score - a.score);

        // 显示结果
        displayResults(results.slice(0, 10), query);
    }

    // 移除 HTML 标签
    function stripHtml(html) {
        const tmp = document.createElement('div');
        tmp.innerHTML = html;
        return tmp.textContent || tmp.innerText || '';
    }

    // 获取匹配文本的上下文摘录
    function getExcerpt(text, query, maxLength) {
        const index = text.toLowerCase().indexOf(query.toLowerCase());
        if (index === -1) return text.substring(0, maxLength) + '...';

        const start = Math.max(0, index - 50);
        const end = Math.min(text.length, index + query.length + 100);
        
        let excerpt = text.substring(start, end);
        if (start > 0) excerpt = '...' + excerpt;
        if (end < text.length) excerpt = excerpt + '...';
        
        return excerpt;
    }

    // 高亮匹配的文本
    function highlightText(text, query) {
        if (!query) return text;
        
        const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
        return text.replace(regex, '<span class="search-highlight">$1</span>');
    }

    // 转义正则表达式特殊字符
    function escapeRegex(str) {
        return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    // 显示搜索结果
    function displayResults(results, query) {
        if (results.length === 0) {
            searchResults.innerHTML = `
                <div class="search-result-item" style="color: #999; text-align: center;">
                    未找到匹配的文章
                </div>
            `;
            searchResults.style.display = 'block';
            return;
        }

        let html = '';
        results.forEach(result => {
            const highlightedTitle = highlightText(result.title, query);
            const highlightedExcerpt = highlightText(result.excerpt, query);
            
            html += `
                <div class="search-result-item" onclick="window.location.href='/${result.path}'">
                    <div class="search-result-title">${highlightedTitle}</div>
                    <div class="search-result-excerpt">${highlightedExcerpt}</div>
                </div>
            `;
        });

        searchResults.innerHTML = html;
        searchResults.style.display = 'block';
    }

    // 监听搜索框输入
    searchBox.addEventListener('input', function(e) {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            performSearch(e.target.value);
        }, 300); // 延迟300ms执行搜索，避免频繁搜索
    });

    // 点击其他地方关闭搜索结果
    document.addEventListener('click', function(e) {
        if (!searchBox.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });

    // 点击搜索框时，如果有内容则显示结果
    searchBox.addEventListener('focus', function() {
        if (searchBox.value.trim().length >= 2) {
            performSearch(searchBox.value);
        }
    });

    // 支持键盘导航
    searchBox.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            searchResults.style.display = 'none';
            searchBox.blur();
        }
    });
})();