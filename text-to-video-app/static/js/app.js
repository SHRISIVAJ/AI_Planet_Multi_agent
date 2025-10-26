// Text to Video App JavaScript

class TextToVideoApp {
    constructor() {
        this.currentJobId = null;
        this.statusCheckInterval = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupCharacterCounter();
    }

    setupEventListeners() {
        const form = document.getElementById('textForm');
        form.addEventListener('submit', (e) => this.handleFormSubmit(e));

        const textInput = document.getElementById('text_input');
        const fileInput = document.getElementById('text_file');

        textInput.addEventListener('input', () => this.updateCharacterCounter());
        fileInput.addEventListener('change', (e) => this.handleFileUpload(e));
    }

    setupCharacterCounter() {
        const textInput = document.getElementById('text_input');
        const counterDiv = document.createElement('div');
        counterDiv.className = 'char-counter';
        counterDiv.id = 'charCounter';
        textInput.parentNode.appendChild(counterDiv);
        this.updateCharacterCounter();
    }

    updateCharacterCounter() {
        const textInput = document.getElementById('text_input');
        const counter = document.getElementById('charCounter');
        const length = textInput.value.length;
        const maxLength = parseInt(textInput.getAttribute('maxlength'));

        counter.textContent = `${length}/${maxLength} characters`;
        
        counter.className = 'char-counter';
        if (length > maxLength * 0.9) {
            counter.classList.add('danger');
        } else if (length > maxLength * 0.75) {
            counter.classList.add('warning');
        }
    }

    handleFileUpload(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const textInput = document.getElementById('text_input');
                textInput.value = e.target.result;
                this.updateCharacterCounter();
            };
            reader.readAsText(file);
        }
    }

    async handleFormSubmit(event) {
        event.preventDefault();
        
        const textInput = document.getElementById('text_input').value.trim();
        const fileInput = document.getElementById('text_file');

        if (!textInput && !fileInput.files[0]) {
            this.showAlert('Please enter some text or upload a file.', 'warning');
            return;
        }

        if (textInput && textInput.length < 10) {
            this.showAlert('Text must be at least 10 characters long.', 'warning');
            return;
        }

        this.showProcessingSection();
        this.hideResultsSection();
        this.hideErrorSection();

        try {
            const formData = new FormData(document.getElementById('textForm'));
            
            const response = await fetch('/process_text', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                this.currentJobId = result.job_id;
                this.startStatusPolling();
            } else {
                this.showError(result.error || 'An error occurred while processing your request.');
            }
        } catch (error) {
            this.showError('Network error. Please check your connection and try again.');
        }
    }

    startStatusPolling() {
        if (this.statusCheckInterval) {
            clearInterval(this.statusCheckInterval);
        }

        this.statusCheckInterval = setInterval(() => {
            this.checkStatus();
        }, 2000); // Check every 2 seconds
    }

    async checkStatus() {
        if (!this.currentJobId) return;

        try {
            const response = await fetch(`/status/${this.currentJobId}`);
            const status = await response.json();

            if (response.ok) {
                this.updateProgress(status.progress, status.message);

                if (status.status === 'completed') {
                    this.showResults(status.video_path);
                    this.stopStatusPolling();
                } else if (status.status === 'error') {
                    this.showError(status.message);
                    this.stopStatusPolling();
                }
            } else {
                this.showError('Failed to check processing status.');
                this.stopStatusPolling();
            }
        } catch (error) {
            this.showError('Error checking status. Please refresh the page.');
            this.stopStatusPolling();
        }
    }

    stopStatusPolling() {
        if (this.statusCheckInterval) {
            clearInterval(this.statusCheckInterval);
            this.statusCheckInterval = null;
        }
    }

    updateProgress(progress, message) {
        const progressBar = document.getElementById('progressBar');
        const statusMessage = document.getElementById('statusMessage');

        progressBar.style.width = `${progress}%`;
        progressBar.textContent = `${progress}%`;
        progressBar.setAttribute('aria-valuenow', progress);
        statusMessage.textContent = message;

        if (progress >= 100) {
            progressBar.classList.remove('progress-bar-animated');
        }
    }

    showProcessingSection() {
        document.getElementById('statusSection').style.display = 'block';
        this.scrollToElement('statusSection');
    }

    hideProcessingSection() {
        document.getElementById('statusSection').style.display = 'none';
    }

    showResults(videoPath) {
        this.hideProcessingSection();
        
        const resultsSection = document.getElementById('resultsSection');
        const videoPreview = document.getElementById('videoPreview');
        const downloadBtn = document.getElementById('downloadBtn');

        videoPreview.src = `/preview/${videoPath}`;
        downloadBtn.onclick = () => {
            window.open(`/download/${videoPath}`, '_blank');
        };

        resultsSection.style.display = 'block';
        this.scrollToElement('resultsSection');
    }

    hideResultsSection() {
        document.getElementById('resultsSection').style.display = 'none';
    }

    showError(message) {
        this.hideProcessingSection();
        this.hideResultsSection();
        
        const errorSection = document.getElementById('errorSection');
        const errorMessage = document.getElementById('errorMessage');
        
        errorMessage.textContent = message;
        errorSection.style.display = 'block';
        this.scrollToElement('errorSection');
    }

    hideErrorSection() {
        document.getElementById('errorSection').style.display = 'none';
    }

    showAlert(message, type = 'info') {
        // Create alert element
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Insert at top of container
        const container = document.querySelector('.container-fluid .row').firstElementChild;
        container.insertBefore(alertDiv, container.firstChild);

        // Auto dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    scrollToElement(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });
        }
    }

    // Utility method to reset the form
    resetForm() {
        document.getElementById('textForm').reset();
        this.updateCharacterCounter();
        this.hideProcessingSection();
        this.hideResultsSection();
        this.hideErrorSection();
        this.currentJobId = null;
        this.stopStatusPolling();
    }
}

// Initialize the app when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const app = new TextToVideoApp();
    
    // Expose app instance globally for debugging
    window.textToVideoApp = app;
    
    // Add some keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl+Enter to submit form
        if (e.ctrlKey && e.key === 'Enter') {
            const form = document.getElementById('textForm');
            form.dispatchEvent(new Event('submit'));
        }
        
        // Escape to reset form
        if (e.key === 'Escape') {
            if (confirm('Reset the form and cancel current operation?')) {
                app.resetForm();
            }
        }
    });
});

// Add some utility functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatDuration(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    
    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
}
