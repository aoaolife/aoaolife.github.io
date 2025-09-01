document.addEventListener('DOMContentLoaded', function() {
    // Touch swipe navigation
    let touchStartX = 0;
    let touchEndX = 0;

    document.addEventListener('touchstart', function(event) {
        touchStartX = event.changedTouches[0].screenX;
    });

    document.addEventListener('touchend', function(event) {
        touchEndX = event.changedTouches[0].screenX;
        handleSwipe();
    });

    function handleSwipe() {
        const swipeDistance = touchEndX - touchStartX;
        if (swipeDistance > 50 && "{{ prev_page }}") {
            window.location.href = "/{{ prev_page }}";
        } else if (swipeDistance < -50 && "{{ next_page }}") {
            window.location.href = "/{{ next_page }}";
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
});