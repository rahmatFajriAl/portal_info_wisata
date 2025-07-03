// Custom JavaScript untuk Django Admin

document.addEventListener('DOMContentLoaded', function() {
    console.log('Custom admin JS loaded!');
    
    // Add smooth scrolling to all internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
    
    // Add loading spinner untuk form submissions
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = form.querySelector('[type="submit"]');
            if (submitButton) {
                submitButton.innerHTML = 'Menyimpan...';
                submitButton.disabled = true;
            }
        });
    });
    
    // Add tooltip untuk icons
    const icons = document.querySelectorAll('[title]');
    icons.forEach(icon => {
        icon.style.cursor = 'help';
    });
    
    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    });
    
    // Add confirmation untuk delete actions
    const deleteButtons = document.querySelectorAll('a[href*="delete"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Apakah Anda yakin ingin menghapus item ini?')) {
                e.preventDefault();
            }
        });
    });
    
    // Add search highlight
    const searchInput = document.querySelector('#searchbar');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = document.querySelectorAll('#result_list tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (searchTerm && text.includes(searchTerm)) {
                    row.style.backgroundColor = '#fef3cd';
                } else {
                    row.style.backgroundColor = '';
                }
            });
        });
    }
});