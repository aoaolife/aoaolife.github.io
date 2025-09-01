document.addEventListener('DOMContentLoaded', function() {
    // 获取导航链接信息
    const prevPageLink = document.querySelector('.nav-arrow-left');
    const nextPageLink = document.querySelector('.nav-arrow-right');

    let prevPageUrl = null;
    let nextPageUrl = null;

    if (prevPageLink) {
        prevPageUrl = prevPageLink.getAttribute('href');
    }
    if (nextPageLink) {
        nextPageUrl = nextPageLink.getAttribute('href');
    }

    // Touch swipe navigation - 修复模板变量问题
    let touchStartX = 0;
    let touchEndX = 0;
    let touchStartY = 0;
    let touchEndY = 0;

    document.addEventListener('touchstart', function(event) {
        touchStartX = event.changedTouches[0].screenX;
        touchStartY = event.changedTouches[0].screenY;
    });

    document.addEventListener('touchend', function(event) {
        touchEndX = event.changedTouches[0].screenX;
        touchEndY = event.changedTouches[0].screenY;
        handleSwipe();
    });

    function handleSwipe() {
        const swipeDistanceX = touchEndX - touchStartX;
        const swipeDistanceY = touchEndY - touchStartY;

        // 只有在水平滑动距离大于垂直滑动距离时才触发页面切换
        // 这样可以避免在垂直滚动时误触发页面切换
        if (Math.abs(swipeDistanceX) > Math.abs(swipeDistanceY) && Math.abs(swipeDistanceX) > 80) {
            if (swipeDistanceX > 80 && prevPageUrl) {
                // 向右滑动，跳转到上一页
                window.location.href = prevPageUrl;
            } else if (swipeDistanceX < -80 && nextPageUrl) {
                // 向左滑动，跳转到下一页
                window.location.href = nextPageUrl;
            }
        }
    }

    // Tree view functionality
    const treeItems = document.querySelectorAll('.tree-item');

    treeItems.forEach(item => {
        const node = item.querySelector('.tree-node');
        const toggle = item.querySelector('.tree-toggle');
        const arrow = item.querySelector('.tree-arrow');
        const children = item.querySelector('.tree-children');

        if (toggle && arrow && children) {
            node.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();

                // Toggle expanded state
                item.classList.toggle('expanded');

                // Update arrow rotation
                if (item.classList.contains('expanded')) {
                    arrow.style.transform = 'rotate(90deg)';
                    children.style.display = 'block';
                } else {
                    arrow.style.transform = 'rotate(0deg)';
                    children.style.display = 'none';
                }
            });
        }
    });

    // Auto-expand tree items that contain the current page
    const currentPath = window.location.pathname;
    const currentLinks = document.querySelectorAll('.tree-link');

    currentLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            // Highlight current page
            link.style.fontWeight = 'bold';
            link.style.backgroundColor = 'rgba(29, 155, 240, 0.1)';
            link.style.borderRadius = '4px';
            link.style.padding = '2px 6px';

            // Expand parent directories
            let parent = link.closest('.tree-item');
            while (parent) {
                const parentContainer = parent.closest('.tree-children');
                if (parentContainer) {
                    const parentItem = parentContainer.previousElementSibling?.closest('.tree-item');
                    if (parentItem) {
                        parentItem.classList.add('expanded');
                        const arrow = parentItem.querySelector('.tree-arrow');
                        if (arrow) {
                            arrow.style.transform = 'rotate(90deg)';
                        }
                        parentContainer.style.display = 'block';
                        parent = parentItem;
                    } else {
                        break;
                    }
                } else {
                    break;
                }
            }
        }
    });

    // Initialize tree state - collapse all by default except expanded ones
    const allTreeItems = document.querySelectorAll('.tree-item');
    allTreeItems.forEach(item => {
        const children = item.querySelector('.tree-children');
        const arrow = item.querySelector('.tree-arrow');

        if (children && !item.classList.contains('expanded')) {
            children.style.display = 'none';
            if (arrow) {
                arrow.style.transform = 'rotate(0deg)';
            }
        }
    });

    // 添加键盘导航支持
    document.addEventListener('keydown', function(event) {
        // 左箭头键 - 上一页
        if (event.key === 'ArrowLeft' && prevPageUrl) {
            window.location.href = prevPageUrl;
        }
        // 右箭头键 - 下一页
        else if (event.key === 'ArrowRight' && nextPageUrl) {
            window.location.href = nextPageUrl;
        }
    });
});