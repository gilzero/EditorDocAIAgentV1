document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.querySelector('.progress-bar');
    const resultContainer = document.getElementById('resultContainer');
    const analysisContent = document.getElementById('analysisContent');
    let currentAnalysis = null;

    // Initialize Feather icons
    feather.replace();

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

    // Export button handler
    document.querySelector('.export-button').addEventListener('click', () => {
        if (currentAnalysis) {
            exportAnalysis(currentAnalysis);
        }
    });

    function handleFile(file) {
        // Validate file type
        const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        if (!validTypes.includes(file.type)) {
            showToast('Please upload a PDF or Word document', 'error');
            return;
        }

        // Validate file size (20MB)
        if (file.size > 20 * 1024 * 1024) {
            showToast('File size must be less than 20MB', 'error');
            return;
        }

        uploadFile(file);
    }

    function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        // Show progress
        progressContainer.classList.remove('d-none');
        resultContainer.classList.add('d-none');
        progressBar.style.width = '0%';

        // Simulate progress until we get the response
        let progress = 0;
        const progressInterval = setInterval(() => {
            if (progress < 90) {
                progress += Math.random() * 10;
                progressBar.style.width = `${Math.min(90, progress)}%`;
            }
        }, 500);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            clearInterval(progressInterval);
            progressBar.style.width = '100%';
            setTimeout(() => {
                progressContainer.classList.add('d-none');
                showResults(data);
            }, 500);
            showToast('Document processed successfully', 'success');
        })
        .catch(error => {
            clearInterval(progressInterval);
            showToast(error.message || 'Error processing document', 'error');
            progressContainer.classList.add('d-none');
        });
    }

    function showResults(data) {
        currentAnalysis = data;
        // Display analysis
        analysisContent.innerHTML = `
            <div class="card">
                <div class="card-body">
                    <h6>Summary</h6>
                    <p>${data.analysis.summary}</p>
                </div>
            </div>
        `;

        resultContainer.classList.remove('d-none');
    }

    function exportAnalysis(data) {
        const content = JSON.stringify(data, null, 2);
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

    function showToast(message, type) {
        Toastify({
            text: message,
            duration: 3000,
            gravity: "top",
            position: 'right',
            style: {
                background: type === 'error' ? '#dc3545' : '#198754'
            },
            className: "custom-toast"
        }).showToast();
    }
});