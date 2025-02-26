// Main JavaScript for FlaskBlog

document.addEventListener('DOMContentLoaded', function() {
    // Enable Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Initialize highlight.js for code blocks
    document.querySelectorAll('pre code').forEach((el) => {
        hljs.highlightElement(el);
    });

    // Confirm before deleting posts, comments, etc.
    document.querySelectorAll('.delete-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm('Are you sure you want to delete this? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Handle slug generation from title
    const titleInput = document.getElementById('title');
    const slugInput = document.getElementById('slug');

    if (titleInput && slugInput) {
        titleInput.addEventListener('blur', function() {
            if (slugInput.value === '') {
                // Generate slug from title
                let slug = titleInput.value
                    .toLowerCase()
                    .trim()
                    .replace(/[^\w\s-]/g, '')
                    .replace(/[\s_-]+/g, '-')
                    .replace(/^-+|-+$/g, '');
                
                slugInput.value = slug;
            }
        });
    }
});
