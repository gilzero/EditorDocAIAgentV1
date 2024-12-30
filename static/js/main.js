function updateLoadingState(step, progress) {
    const steps = ['uploadStep', 'processStep', 'analyzeStep'];
    const progressBar = document.querySelector('.loading-progress-bar');

    // Update progress bar
    progressBar.style.width = `${progress}%`;

    // Update steps
    steps.forEach((stepId, index) => {
        const stepElement = document.getElementById(stepId);
        if (index < steps.indexOf(step)) {
            stepElement.classList.remove('active');
            stepElement.classList.add('completed');
            const icon = stepElement.querySelector('i');
            icon.setAttribute('data-feather', 'check-circle');
        } else if (stepId === step) {
            stepElement.classList.add('active');
            stepElement.classList.remove('completed');
        } else {
            stepElement.classList.remove('active', 'completed');
        }
    });

    // Update Feather icons
    feather.replace();
}

// Global function for toggling sections
window.toggleSection = function(sectionId) {
    const header = document.querySelector(`[aria-controls="section-${sectionId}"]`);
    const content = document.getElementById(`section-${sectionId}`);
    if (!header || !content) return;

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

    // Drag and drop handlers
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
        const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        if (!validTypes.includes(file.type)) {
            showError('Please upload a PDF or Word document');
            return;
        }

        if (file.size > 20 * 1024 * 1024) {
            showError('File size must be less than 20MB');
            return;
        }

        uploadFile(file);
    }

    function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        progressContainer.classList.remove('d-none');
        paymentContainer.classList.add('d-none');
        resultContainer.classList.add('d-none');

        // Show upload step
        updateLoadingState('uploadStep', 0);

        // Simulate upload progress
        let progress = 0;
        const uploadInterval = setInterval(() => {
            progress += 5;
            if (progress <= 30) {
                updateLoadingState('uploadStep', progress);
            } else {
                clearInterval(uploadInterval);
            }
        }, 100);

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
            clearInterval(uploadInterval);
            updateLoadingState('processStep', 60);
            return response.json();
        })
        .then(data => {
            // Show processing step
            setTimeout(() => {
                updateLoadingState('analyzeStep', 90);
                setTimeout(() => {
                    progressContainer.classList.add('d-none');
                    setupStripePayment(data);
                    showToast('Document uploaded successfully', 'success');
                }, 1000);
            }, 1000);
        })
        .catch(error => {
            clearInterval(uploadInterval);
            showError(error.message || 'Error processing document');
            progressContainer.classList.add('d-none');
        });
    }

    function setupStripePayment(data) {
        currentDocumentId = data.document_id;
        clientSecret = data.client_secret;

        // Initialize Stripe with Alipay
        stripe = Stripe(data.publishable_key);
        elements = stripe.elements({
            clientSecret: data.client_secret,
            appearance: {
                theme: 'stripe'
            }
        });

        // Create payment element with additional payment methods
        const paymentElement = elements.create('payment', {
            layout: {
                type: 'tabs',
                defaultCollapsed: false
            }
        });

        paymentElement.mount('#card-element');

        // Handle form submission
        const form = document.getElementById('payment-form');
        form.addEventListener('submit', handlePaymentSubmission);

        // Show payment form and trigger confetti
        paymentContainer.classList.remove('d-none');

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
            // Confirm the payment using PaymentElement
            const {error} = await stripe.confirmPayment({
                elements,
                confirmParams: {
                    return_url: window.location.origin,
                },
                redirect: 'if_required'
            });

            if (error) {
                throw new Error(error.message);
            }

            // If we get here without a redirect, payment was successful
            const response = await fetch('/payment/success', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    payment_intent_id: clientSecret.split('_secret_')[0],
                    document_id: currentDocumentId,
                    analysis_options: getAnalysisOptions()
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
            submitButton.textContent = 'Pay ¥3';
        }
    }

    function getAnalysisOptions() {
        return {
            characterAnalysis: document.getElementById('characterAnalysis').checked,
            plotAnalysis: document.getElementById('plotAnalysis').checked,
            thematicAnalysis: document.getElementById('thematicAnalysis').checked,
            readabilityAssessment: document.getElementById('readabilityAssessment').checked,
            sentimentAnalysis: document.getElementById('sentimentAnalysis').checked,
            styleConsistency: document.getElementById('styleConsistency').checked
        };
    }

    function showResults(data) {
        currentAnalysis = data;
        const analysisContent = data.analysis.summary;
        const accordion = document.getElementById('analysisAccordion');
        accordion.innerHTML = ''; // Clear existing content

        // Define the sections to extract from the analysis
        const sections = [
            { id: 'summary', title: '摘要：', icon: 'file-text', regex: /摘要：[\s\S]*?(?=\n*人物分析：|$)/},
            { id: 'characters', title: '人物分析：', icon: 'users', regex: /人物分析：[\s\S]*?(?=\n*情节分析：|$)/},
            { id: 'plot', title: '情节分析：', icon: 'book-open', regex: /情节分析：[\s\S]*?(?=\n*主题分析：|$)/},
            { id: 'themes', title: '主题分析：', icon: 'feather', regex: /主题分析：[\s\S]*?(?=\n*可读性评估：|$)/},
            { id: 'readability', title: '可读性评估：', icon: 'check-circle', regex: /可读性评估：[\s\S]*?(?=\n*情感分析：|$)/},
            { id: 'sentiment', title: '情感分析：', icon: 'heart', regex: /情感分析：[\s\S]*?(?=\n*风格和一致性：|$)/},
            { id: 'style', title: '风格和一致性：', icon: 'edit-3', regex: /风格和一致性：[\s\S]*?(?=$)/}
        ];

        // Extract content for each section using improved regex
        sections.forEach((section, index) => {
            const match = analysisContent.match(section.regex);
            let content = match ? match[0] : '暂无内容';

            // Remove the section title and colon from the content
            content = content.replace(new RegExp(`^${section.title}`), '').trim();

            // Remove any numbers at start of lines and extra whitespace
            content = content.replace(/^\d+\.\s*/gm, '').trim();

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
                            ${section.title.replace('：', '')}
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
        setTimeout(() => toggleSection('summary'), 100);
    }

    function formatContent(content) {
        if (!content || content === '暂无内容') {
            return content;
        }

        // Remove any remaining section numbers and clean up whitespace
        content = content.replace(/^\d+\.\s*/gm, '')
                        .replace(/^#+\s*|^\s+/gm, '')
                        .trim();

        // Convert markdown-style lists to HTML
        content = content.replace(/- (.*?)(?=\n|$)/g, '<li>$1</li>');
        if (content.includes('<li>')) {
            content = '<ul>' + content + '</ul>';
        }

        // Convert bold text
        content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        // Convert paragraphs (only create paragraphs for actual multi-line breaks)
        content = content
            .split(/\n{2,}/)
            .map(p => p.trim())
            .filter(p => p)
            .map(p => `<p>${p}</p>`)
            .join('');

        return content || '暂无内容';
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

        dropZone.parentNode.insertBefore(errorDiv, dropZone);
        feather.replace();

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
            }
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