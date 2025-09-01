document.addEventListener('DOMContentLoaded', function() {
    // Get navigation URLs from the page context
    const prevPageElement = document.querySelector('.nav-prev, .pagination-prev');
    const nextPageElement = document.querySelector('.nav-next, .pagination-next');

    const prevPageUrl = prevPageElement ? prevPageElement.getAttribute('href') : null;
    const nextPageUrl = nextPageElement ? nextPageElement.getAttribute('href') : null;

    // Touch swipe navigation with improved detection
    let touchStartX = 0;
    let touchStartY = 0;
    let touchEndX = 0;
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
        const swipeDistanceY = Math.abs(touchEndY - touchStartY);

        // Only trigger swipe if horizontal distance is greater than vertical (not scrolling)
        if (Math.abs(swipeDistanceX) > 80 && swipeDistanceY < 100) {
            if (swipeDistanceX > 0 && prevPageUrl) {
                // Swipe right - go to previous page
                window.location.href = prevPageUrl;
            } else if (swipeDistanceX < 0 && nextPageUrl) {
                // Swipe left - go to next page
                window.location.href = nextPageUrl;
            }
        }
    }

    // Keyboard navigation
    document.addEventListener('keydown', function(event) {
        // Prevent navigation when user is typing in an input field
        if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
            return;
        }

        switch(event.key) {
            case 'ArrowLeft':
                if (prevPageUrl) {
                    window.location.href = prevPageUrl;
                }
                break;
            case 'ArrowRight':
                if (nextPageUrl) {
                    window.location.href = nextPageUrl;
                }
                break;
        }
    });

    // Tree view functionality with improved state management
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

                // Update arrow rotation and children visibility
                if (item.classList.contains('expanded')) {
                    arrow.style.transform = 'rotate(90deg)';
                    children.style.display = 'block';

                    // Save expanded state
                    localStorage.setItem(`tree-${getTreePath(item)}`, 'expanded');
                } else {
                    arrow.style.transform = 'rotate(0deg)';
                    children.style.display = 'none';

                    // Remove saved state
                    localStorage.removeItem(`tree-${getTreePath(item)}`);
                }
            });
        }
    });

    // Helper function to get tree path for state persistence
    function getTreePath(item) {
        const toggle = item.querySelector('.tree-toggle');
        if (!toggle) return '';

        let path = toggle.textContent.trim();
        let parent = item.closest('.tree-children');

        while (parent) {
            const parentItem = parent.previousElementSibling?.closest('.tree-item');
            if (parentItem) {
                const parentToggle = parentItem.querySelector('.tree-toggle');
                if (parentToggle) {
                    path = parentToggle.textContent.trim() + '/' + path;
                }
                parent = parentItem.closest('.tree-children');
            } else {
                break;
            }
        }

        return path;
    }

    // Restore tree state from localStorage
    function restoreTreeState() {
        treeItems.forEach(item => {
            const treePath = getTreePath(item);
            if (treePath && localStorage.getItem(`tree-${treePath}`) === 'expanded') {
                item.classList.add('expanded');
                const arrow = item.querySelector('.tree-arrow');
                const children = item.querySelector('.tree-children');
                if (arrow) arrow.style.transform = 'rotate(90deg)';
                if (children) children.style.display = 'block';
            }
        });
    }

    // Auto-expand tree items that contain the current page
    const currentPath = window.location.pathname;
    const currentLinks = document.querySelectorAll('.tree-link');

    currentLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            // Highlight current page
            link.style.fontWeight = 'bold';
            link.style.backgroundColor = 'rgba(29, 155, 240, 0.15)';
            link.style.borderRadius = '4px';
            link.style.padding = '2px 6px';

            // Expand parent directories
            let parent = link.closest('.tree-item');
            while (parent) {
                const parentContainer = parent.closest('.tree-children');
                if (parentContainer) {
                    const parentItem = parentContainer.previousElementSibling?.closest('.tree-item');
                    if (parentItem && parentItem.querySelector('.tree-toggle')) {
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

    // Restore previously expanded state
    restoreTreeState();

    // Smooth scroll for internal links
    const internalLinks = document.querySelectorAll('a[href^="#"]');
    internalLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading animation for navigation
    const navButtons = document.querySelectorAll('.nav-btn, .pagination-btn');
    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.style.opacity = '0.7';
            this.style.transform = 'scale(0.95)';
        });
    });
});