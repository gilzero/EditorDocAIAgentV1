document.addEventListener('DOMContentLoaded', function() {
    // Initialize variables
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const progressContainer = document.getElementById('progressContainer');
    const paymentContainer = document.getElementById('paymentContainer');
    const resultContainer = document.getElementById('resultContainer');
    const analysisContent = document.getElementById('analysisContent');
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    let stripe;
    let elements;
    let currentDocumentId;
    let clientSecret;
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
        paymentContainer.classList.add('d-none');
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
            setupStripePayment(data);
            showToast('Document uploaded successfully', 'success');
        })
        .catch(error => {
            showError(error.message || 'Error processing document');
            progressContainer.classList.add('d-none');
        });
    }

    function setupStripePayment(data) {
        currentDocumentId = data.document_id;
        clientSecret = data.client_secret;

        // Initialize Stripe
        stripe = Stripe(data.publishable_key);
        elements = stripe.elements();

        // Create card element
        const cardElement = elements.create('card');
        cardElement.mount('#card-element');

        // Handle form submission
        const form = document.getElementById('payment-form');
        form.addEventListener('submit', handlePaymentSubmission);

        // Show payment form and trigger confetti
        paymentContainer.classList.remove('d-none');

        // Trigger confetti animation
        confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 },
            colors: ['#0d6efd', '#198754', '#ffc107']
        });
    }

    async function handlePaymentSubmission(event) {
        event.preventDefault();

        const submitButton = document.getElementById('submit-payment');
        submitButton.disabled = true;
        submitButton.textContent = 'Processing...';

        try {
            const {error, paymentIntent} = await stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: elements.getElement('card'),
                }
            });

            if (error) {
                throw new Error(error.message);
            }

            // Payment successful, get analysis results
            const response = await fetch('/payment/success', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    payment_intent_id: paymentIntent.id,
                    document_id: currentDocumentId
                })
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Error processing payment');
            }

            paymentContainer.classList.add('d-none');
            showResults(result);
            showToast('Payment successful', 'success');

        } catch (error) {
            showError(error.message || 'Payment failed');
            submitButton.disabled = false;
            submitButton.textContent = 'Pay $0.50';
        }
    }

    function showResults(data) {
        currentAnalysis = data;
        const analysisContent = data.analysis.summary;
        const accordion = document.getElementById('analysisAccordion');
        accordion.innerHTML = ''; // Clear existing content

        // Define the sections to extract from the analysis
        const sections = [
            { id: 'summary', title: '摘要', icon: 'file-text' },
            { id: 'characters', title: '人物分析', icon: 'users' },
            { id: 'plot', title: '情节分析', icon: 'book-open' },
            { id: 'themes', title: '主题分析', icon: 'feather' },
            { id: 'readability', title: '可读性评估', icon: 'check-circle' },
            { id: 'sentiment', title: '情感分析', icon: 'heart' },
            { id: 'style', title: '风格和一致性', icon: 'edit-3' }
        ];

        // Extract content for each section using regex
        sections.forEach((section, index) => {
            const sectionRegex = new RegExp(`${section.title}[：:](.*?)(?=\\n\\n|$)`, 's');
            const match = analysisContent.match(sectionRegex);
            const content = match ? match[1].trim() : '暂无内容';

            // Create section HTML
            const sectionHtml = `
                <div class="analysis-section-wrapper">
                    <div class="analysis-section-header" 
                         role="button"
                         aria-expanded="false"
                         aria-controls="section-${section.id}"
                         tabindex="0"
                         onclick="toggleSection('${section.id}')">
                        <h6>
                            <i data-feather="${section.icon}" aria-hidden="true"></i>
                            ${section.title}
                        </h6>
                        <i data-feather="chevron-down" class="chevron-icon" aria-hidden="true"></i>
                    </div>
                    <div id="section-${section.id}" 
                         class="analysis-section-content"
                         role="region"
                         aria-labelledby="header-${section.id}">
                        <div class="analysis-content">${formatContent(content)}</div>
                    </div>
                </div>
            `;
            accordion.innerHTML += sectionHtml;
        });

        // Initialize Feather icons for the new content
        feather.replace();
        resultContainer.classList.remove('d-none');

        // Automatically expand the first section
        toggleSection('summary');
    }

    function formatContent(content) {
        // Convert markdown-style lists to HTML
        content = content.replace(/- (.*?)(?=\n|$)/g, '<li>$1</li>');
        if (content.includes('<li>')) {
            content = '<ul>' + content + '</ul>';
        }

        // Convert bold text
        content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        // Convert paragraphs
        content = content.split('\n\n').map(p => `<p>${p}</p>`).join('');

        return content;
    }

    function toggleSection(sectionId) {
        const header = document.querySelector(`[aria-controls="section-${sectionId}"]`);
        const content = document.getElementById(`section-${sectionId}`);
        const isExpanded = header.getAttribute('aria-expanded') === 'true';

        // Toggle aria-expanded
        header.setAttribute('aria-expanded', !isExpanded);

        // Toggle content visibility
        content.classList.toggle('active');

        // Announce to screen readers
        if (!isExpanded) {
            content.focus();
        }
    }

    // Add keyboard support for section headers
    document.addEventListener('keydown', function(event) {
        if (event.target.classList.contains('analysis-section-header')) {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                const sectionId = event.target.getAttribute('aria-controls').replace('section-', '');
                toggleSection(sectionId);
            }
        }
    });


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
    document.querySelector('.export-button')?.addEventListener('click', () => {
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