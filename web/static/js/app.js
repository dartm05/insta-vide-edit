// Global variables
let currentJobId = null;
let statusCheckInterval = null;
let selectedPresetId = null;

// Tab switching
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from all buttons
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName).classList.add('active');

    // Add active class to clicked button
    event.target.classList.add('active');
}

// File input display
function setupFileInputs() {
    const fileInputs = [
        { input: 'referenceVideo', display: 'refFileName' },
        { input: 'inputVideo', display: 'inputFileName' },
        { input: 'presetVideo', display: 'presetFileName' },
        { input: 'convertVideo', display: 'convertFileName' }
    ];

    fileInputs.forEach(({ input, display }) => {
        const inputEl = document.getElementById(input);
        const displayEl = document.getElementById(display);

        if (inputEl && displayEl) {
            inputEl.addEventListener('change', (e) => {
                const fileName = e.target.files[0]?.name || 'No file chosen';
                displayEl.textContent = fileName;
            });
        }
    });
}

// Preset selection
function selectPreset(presetId) {
    selectedPresetId = presetId;
    document.getElementById('selectedPreset').value = presetId;

    // Update UI
    document.querySelectorAll('.preset-card').forEach(card => {
        card.classList.remove('selected');
    });

    event.currentTarget.classList.add('selected');
}

// Show/hide sections
function showSection(sectionId) {
    const sections = ['progressSection', 'resultSection', 'errorSection'];
    sections.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.style.display = id === sectionId ? 'block' : 'none';
        }
    });

    // Hide all forms
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.display = tab.id === sectionId ? 'none' :
            (tab.classList.contains('active') ? 'block' : 'none');
    });
}

// Update progress bar
function updateProgress(progress, text = '') {
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');

    if (progressFill) {
        progressFill.style.width = `${progress}%`;
    }

    if (progressText && text) {
        progressText.textContent = text;
    }
}

// Start status checking
function startStatusCheck(jobId) {
    currentJobId = jobId;

    // Clear any existing interval
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
    }

    // Check status every 2 seconds
    statusCheckInterval = setInterval(() => {
        checkJobStatus(jobId);
    }, 2000);

    // Check immediately
    checkJobStatus(jobId);
}

// Check job status
async function checkJobStatus(jobId) {
    try {
        const response = await fetch(`/api/status/${jobId}`);

        if (!response.ok) {
            throw new Error('Failed to check status');
        }

        const job = await response.json();

        // Update progress
        updateProgress(job.progress, getStatusText(job));

        // Handle different statuses
        if (job.status === 'completed') {
            clearInterval(statusCheckInterval);
            showSuccess(jobId);
        } else if (job.status === 'failed') {
            clearInterval(statusCheckInterval);
            showError(job.error || 'Processing failed');
        }

    } catch (error) {
        console.error('Status check error:', error);
    }
}

// Get status text
function getStatusText(job) {
    const progress = job.progress;

    if (progress < 20) return 'Starting...';
    if (progress < 40) return 'Analyzing video...';
    if (progress < 60) return 'Learning style...';
    if (progress < 80) return 'Applying edits...';
    if (progress < 100) return 'Finalizing...';
    return 'Complete!';
}

// Show success
function showSuccess(jobId) {
    showSection('resultSection');
    updateProgress(100, 'Processing complete!');
}

// Show error
function showError(message) {
    showSection('errorSection');
    const errorText = document.getElementById('errorText');
    if (errorText) {
        errorText.textContent = message;
    }
}

// Download result
async function downloadResult() {
    if (!currentJobId) return;

    try {
        const response = await fetch(`/api/download/${currentJobId}`);

        if (!response.ok) {
            throw new Error('Download failed');
        }

        // Get filename from Content-Disposition header or use default
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = 'video.mp4';
        if (contentDisposition) {
            const matches = /filename="?([^"]+)"?/.exec(contentDisposition);
            if (matches) filename = matches[1];
        }

        // Download file
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

    } catch (error) {
        console.error('Download error:', error);
        alert('Failed to download video');
    }
}

// Reset form
function resetForm() {
    // Clear interval
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
    }

    // Hide result/error sections
    document.getElementById('resultSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
    document.getElementById('progressSection').style.display = 'none';

    // Show tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        if (tab.classList.contains('active')) {
            tab.style.display = 'block';
        }
    });

    // Reset forms
    document.querySelectorAll('form').forEach(form => form.reset());

    // Reset file displays
    document.querySelectorAll('.file-name').forEach(el => {
        el.textContent = 'No file chosen';
    });

    // Reset preset selection
    selectedPresetId = null;
    document.querySelectorAll('.preset-card').forEach(card => {
        card.classList.remove('selected');
    });

    // Reset job
    currentJobId = null;
}

// Style Transfer Form
document.getElementById('styleTransferForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const referenceVideo = document.getElementById('referenceVideo').files[0];
    const inputVideo = document.getElementById('inputVideo').files[0];
    const format = document.getElementById('styleFormat').value;
    const styleName = document.getElementById('styleName').value;

    if (!referenceVideo || !inputVideo) {
        alert('Please select both videos');
        return;
    }

    // Create form data
    const formData = new FormData();
    formData.append('reference_video', referenceVideo);
    formData.append('input_video', inputVideo);
    formData.append('format', format);
    if (styleName) {
        formData.append('style_name', styleName);
    }

    // Show progress
    showSection('progressSection');
    updateProgress(0, 'Uploading...');

    try {
        const response = await fetch('/api/style-transfer', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }

        const result = await response.json();
        startStatusCheck(result.job_id);

    } catch (error) {
        console.error('Upload error:', error);
        showError(error.message);
    }
});

// Preset Form
document.getElementById('presetForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const video = document.getElementById('presetVideo').files[0];
    const preset = document.getElementById('selectedPreset').value;
    const format = document.getElementById('presetFormat').value;

    if (!video) {
        alert('Please select a video');
        return;
    }

    if (!preset) {
        alert('Please select a preset style');
        return;
    }

    // Create form data
    const formData = new FormData();
    formData.append('video', video);
    formData.append('preset', preset);
    formData.append('format', format);

    // Show progress
    showSection('progressSection');
    updateProgress(0, 'Uploading...');

    try {
        const response = await fetch('/api/preset-style', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }

        const result = await response.json();
        startStatusCheck(result.job_id);

    } catch (error) {
        console.error('Upload error:', error);
        showError(error.message);
    }
});

// Convert Form
document.getElementById('convertForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const video = document.getElementById('convertVideo').files[0];
    const format = document.getElementById('convertFormat').value;

    if (!video) {
        alert('Please select a video');
        return;
    }

    // Create form data
    const formData = new FormData();
    formData.append('video', video);
    formData.append('format', format);

    // Show progress
    showSection('progressSection');
    updateProgress(0, 'Uploading...');

    try {
        const response = await fetch('/api/convert', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }

        const result = await response.json();
        startStatusCheck(result.job_id);

    } catch (error) {
        console.error('Upload error:', error);
        showError(error.message);
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupFileInputs();
});
