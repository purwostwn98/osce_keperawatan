// Custom JavaScript for OSCE Keperawatan Admin

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize tooltips
    const tooltips = document.querySelectorAll('[data-toggle="tooltip"]');
    tooltips.forEach(function(tooltip) {
        new bootstrap.Tooltip(tooltip);
    });

    // Auto-refresh dashboard metrics every 30 seconds
    if (window.location.pathname === '/admin/') {
        setInterval(function() {
            refreshDashboardMetrics();
        }, 30000);
    }

    // Confirmation dialogs for delete actions
    const deleteButtons = document.querySelectorAll('.deletelink');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Apakah Anda yakin ingin menghapus data ini?')) {
                e.preventDefault();
            }
        });
    });

    // Auto-save form changes
    const forms = document.querySelectorAll('form.auto-save');
    forms.forEach(function(form) {
        let saveTimer;
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(function(input) {
            input.addEventListener('change', function() {
                clearTimeout(saveTimer);
                saveTimer = setTimeout(function() {
                    autoSaveForm(form);
                }, 2000);
            });
        });
    });

    // Search enhancement
    const searchInputs = document.querySelectorAll('input[type="search"]');
    searchInputs.forEach(function(input) {
        let searchTimer;
        input.addEventListener('input', function() {
            clearTimeout(searchTimer);
            searchTimer = setTimeout(function() {
                performSearch(input.value);
            }, 500);
        });
    });

    // Bulk actions
    const selectAllCheckbox = document.querySelector('#select-all');
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            const checkboxes = document.querySelectorAll('.action-select');
            checkboxes.forEach(function(checkbox) {
                checkbox.checked = selectAllCheckbox.checked;
            });
            updateBulkActionButtons();
        });
    }

    // Update bulk action buttons when individual checkboxes change
    const actionCheckboxes = document.querySelectorAll('.action-select');
    actionCheckboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            updateBulkActionButtons();
        });
    });

    // Mobile sidebar toggle
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.unfold-sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
    }

    // Disable sidebar toggle buttons
    disableSidebarToggle();

    // Initialize charts if Chart.js is available
    if (typeof Chart !== 'undefined') {
        initializeDashboardCharts();
    }

    // Export functionality
    const exportButtons = document.querySelectorAll('.export-btn');
    exportButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const format = button.dataset.format;
            const url = button.dataset.url;
            exportData(format, url);
        });
    });

});

function refreshDashboardMetrics() {
    fetch('/admin/dashboard/metrics/')
        .then(response => response.json())
        .then(data => {
            updateMetrics(data);
        })
        .catch(error => {
            console.log('Error refreshing metrics:', error);
        });
}

function updateMetrics(data) {
    Object.keys(data).forEach(function(key) {
        const element = document.getElementById(key);
        if (element) {
            element.textContent = data[key];
        }
    });
}

function autoSaveForm(form) {
    const formData = new FormData(form);
    const saveIcon = form.querySelector('.save-indicator');
    
    if (saveIcon) {
        saveIcon.style.display = 'inline';
    }

    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => {
        if (response.ok) {
            showNotification('Data berhasil disimpan otomatis', 'success');
        } else {
            showNotification('Gagal menyimpan data', 'error');
        }
    })
    .catch(error => {
        showNotification('Error: ' + error.message, 'error');
    })
    .finally(() => {
        if (saveIcon) {
            saveIcon.style.display = 'none';
        }
    });
}

function performSearch(query) {
    if (query.length < 3) return;
    
    // Implement search functionality
    console.log('Searching for:', query);
}

function updateBulkActionButtons() {
    const selectedCheckboxes = document.querySelectorAll('.action-select:checked');
    const bulkActionButtons = document.querySelectorAll('.bulk-action-btn');
    
    if (selectedCheckboxes.length > 0) {
        bulkActionButtons.forEach(button => button.style.display = 'inline-block');
    } else {
        bulkActionButtons.forEach(button => button.style.display = 'none');
    }
}

function initializeDashboardCharts() {
    // Initialize charts based on data attributes
    const chartElements = document.querySelectorAll('[data-chart]');
    
    chartElements.forEach(function(element) {
        const chartData = JSON.parse(element.dataset.chart);
        new Chart(element, chartData);
    });
}

function exportData(format, url) {
    const loading = document.createElement('div');
    loading.className = 'loading-spinner';
    document.body.appendChild(loading);

    fetch(url + '?format=' + format)
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'export.' + format;
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => {
            showNotification('Error exporting data: ' + error.message, 'error');
        })
        .finally(() => {
            document.body.removeChild(loading);
        });
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = 'notification-' + type;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(function() {
        document.body.removeChild(notification);
    }, 3000);
}

// Utility functions
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

function formatDate(date) {
    return new Intl.DateTimeFormat('id-ID').format(new Date(date));
}

// Function to disable sidebar toggle
function disableSidebarToggle() {
    // Find all sidebar toggle elements
    const sidebarToggles = document.querySelectorAll('.material-symbols-outlined[hx-get*="toggle-sidebar"]');
    
    sidebarToggles.forEach(function(toggle) {
        // Disable click events
        toggle.style.pointerEvents = 'none';
        toggle.style.opacity = '0.5';
        toggle.style.cursor = 'not-allowed';
        
        // Remove hx-get attribute to prevent HTMX requests
        toggle.removeAttribute('hx-get');
        
        // Remove Alpine.js click handler
        toggle.removeAttribute('x-on:click');
        
        // Add disabled class
        toggle.classList.add('disabled');
    });
    
    console.log('Sidebar toggle buttons disabled');
}

// Export functions for global use
window.OSCEAdmin = {
    refreshDashboardMetrics,
    updateMetrics,
    autoSaveForm,
    performSearch,
    updateBulkActionButtons,
    exportData,
    showNotification,
    formatNumber,
    disableSidebarToggle,
    formatDate
};
