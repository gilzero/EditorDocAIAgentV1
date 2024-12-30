document.addEventListener('DOMContentLoaded', function() {
    // Initialize variables
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const progressContainer = document.getElementById('progressContainer');
    const resultContainer = document.getElementById('resultContainer');
    const analysisContent = document.getElementById('analysisContent');
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    let currentAnalysis = null;

    // Theme handling
    function initTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);
    }

    function updateThemeIcon(theme) {
        themeIcon.setAttribute('data-feather', theme === 'dark' ? 'sun' : 'moon');
        feather.replace();
    }

    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });

    // Initialize Feather icons
    feather.replace();

    // Initialize theme
    initTheme();

    // Drag and drop handlers with improved feedback
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
        });
    });

    dropZone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files.length) handleFile(files[0]);
    });

    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) handleFile(e.target.files[0]);
    });

    function handleFile(file) {
        // Validate file type with improved error messages
        const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        if (!validTypes.includes(file.type)) {
            showError('Please upload a PDF or Word document');
            return;
        }

        // Validate file size (20MB) with user-friendly message
        if (file.size > 20 * 1024 * 1024) {
            showError('File size must be less than 20MB');
            return;
        }

        uploadFile(file);
    }

    function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        // Show progress animation
        progressContainer.classList.remove('d-none');
        resultContainer.classList.add('d-none');

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'Error processing document');
                });
            }
            return response.json();
        })
        .then(data => {
            progressContainer.classList.add('d-none');
            showResults(data);
            showToast('Document processed successfully', 'success');
        })
        .catch(error => {
            showError(error.message || 'Error processing document');
            progressContainer.classList.add('d-none');
        });
    }

    function showResults(data) {
        currentAnalysis = data;
        analysisContent.innerHTML = `<p>${data.analysis.summary}</p>`;
        resultContainer.classList.remove('d-none');

        // Re-initialize Feather icons for dynamic content
        feather.replace();
    }

    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = `
            <i data-feather="alert-circle"></i>
            <span>${message}</span>
        `;

        // Insert error message before the upload container
        dropZone.parentNode.insertBefore(errorDiv, dropZone);

        // Initialize Feather icons for the error icon
        feather.replace();

        // Remove error message after 5 seconds
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }

    function showToast(message, type) {
        Toastify({
            text: message,
            duration: 3000,
            gravity: "top",
            position: 'right',
            style: {
                background: type === 'error' ? '#ef4444' : '#10b981',
                borderRadius: '6px',
                padding: '12px 24px'
            },
            onClick: function(){} // Callback after click
        }).showToast();
    }

    // Export functionality
    document.querySelector('.export-button').addEventListener('click', () => {
        if (currentAnalysis) {
            const content = JSON.stringify(currentAnalysis, null, 2);
            const blob = new Blob([content], { type: 'application/json' });
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'document-analysis.json';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
        }
    });
});