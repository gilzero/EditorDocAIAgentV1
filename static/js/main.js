document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.querySelector('.progress-bar');
    const resultContainer = document.getElementById('resultContainer');
    const metadataTable = document.getElementById('metadataTable');
    const analysisContent = document.getElementById('analysisContent');

    // Drag and drop handlers
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
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
        progressBar.style.width = '0%';
        resultContainer.classList.add('d-none');

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            showResults(data);
            showToast('Document processed successfully', 'success');
        })
        .catch(error => {
            showToast(error.message || 'Error processing document', 'error');
        })
        .finally(() => {
            progressContainer.classList.add('d-none');
        });
    }

    function showResults(data) {
        // Display metadata
        metadataTable.innerHTML = Object.entries(data.metadata)
            .filter(([key]) => key !== 'text_content')
            .map(([key, value]) => `
                <tr>
                    <td class="text-muted">${key.replace(/_/g, ' ').toUpperCase()}</td>
                    <td>${value}</td>
                </tr>
            `).join('');

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

    function showToast(message, type) {
        Toastify({
            text: message,
            duration: 3000,
            gravity: "top",
            position: 'right',
            backgroundColor: type === 'error' ? '#dc3545' : '#198754',
            className: "custom-toast"
        }).showToast();
    }
});
