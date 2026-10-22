// Preview functionality for video processing

let uploadedVideos = [];
let currentPreviewIndex = 0;

// Handle multiple file uploads
function handleMultipleFileUpload(files, inputType) {
    const fileArray = Array.from(files);

    fileArray.forEach((file, index) => {
        const videoData = {
            id: `video-${Date.now()}-${index}`,
            file: file,
            name: file.name,
            size: (file.size / (1024 * 1024)).toFixed(2) + ' MB',
            type: inputType,
            preview: null,
            status: 'pending'
        };

        uploadedVideos.push(videoData);
        createVideoPreview(videoData);
    });

    updateVideoList();
}

// Create video preview thumbnail
function createVideoPreview(videoData) {
    const video = document.createElement('video');
    video.src = URL.createObjectURL(videoData.file);
    video.currentTime = 1; // Get frame at 1 second

    video.addEventListener('loadeddata', function() {
        const canvas = document.createElement('canvas');
        canvas.width = 320;
        canvas.height = 180;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        videoData.preview = canvas.toDataURL();
        updateVideoList();
        URL.revokeObjectURL(video.src);
    });
}

// Update video list display
function updateVideoList() {
    const container = document.getElementById('videoListContainer');
    if (!container) return;

    if (uploadedVideos.length === 0) {
        container.style.display = 'none';
        return;
    }

    container.style.display = 'block';
    container.innerHTML = '<h3>Uploaded Videos (' + uploadedVideos.length + ')</h3>';

    const listHtml = uploadedVideos.map((video, index) => `
        <div class="video-item ${video.status}" data-index="${index}">
            <div class="video-thumbnail">
                ${video.preview ?
                    `<img src="${video.preview}" alt="${video.name}">` :
                    '<div class="loading-thumbnail">Loading...</div>'
                }
            </div>
            <div class="video-info">
                <div class="video-name">${video.name}</div>
                <div class="video-details">${video.size} • ${video.type}</div>
                <div class="video-status">${getStatusText(video.status)}</div>
            </div>
            <div class="video-actions">
                <button onclick="previewVideo(${index})" class="btn-preview">
                    👁️ Preview
                </button>
                <button onclick="removeVideo(${index})" class="btn-remove">
                    ❌ Remove
                </button>
            </div>
        </div>
    `).join('');

    container.innerHTML += `<div class="video-list">${listHtml}</div>`;

    // Add batch actions
    if (uploadedVideos.length > 0) {
        container.innerHTML += `
            <div class="batch-actions">
                <button onclick="processAllVideos()" class="btn btn-primary">
                    🚀 Process All Videos (${uploadedVideos.length})
                </button>
                <button onclick="clearAllVideos()" class="btn btn-secondary">
                    🗑️ Clear All
                </button>
            </div>
        `;
    }
}

// Get status text with emoji
function getStatusText(status) {
    const statusMap = {
        'pending': '⏳ Pending',
        'processing': '⚙️ Processing...',
        'completed': '✅ Completed',
        'failed': '❌ Failed',
        'previewing': '👁️ Previewing'
    };
    return statusMap[status] || status;
}

// Preview a specific video
function previewVideo(index) {
    currentPreviewIndex = index;
    const video = uploadedVideos[index];

    const previewModal = document.getElementById('previewModal');
    const previewPlayer = document.getElementById('previewPlayer');
    const previewInfo = document.getElementById('previewInfo');

    previewPlayer.src = URL.createObjectURL(video.file);
    previewInfo.innerHTML = `
        <h3>${video.name}</h3>
        <p>Size: ${video.size}</p>
        <p>Type: ${video.type}</p>
    `;

    previewModal.style.display = 'flex';
}

// Close preview modal
function closePreview() {
    const previewModal = document.getElementById('previewModal');
    const previewPlayer = document.getElementById('previewPlayer');

    previewPlayer.pause();
    previewPlayer.src = '';
    previewModal.style.display = 'none';
}

// Remove video from list
function removeVideo(index) {
    uploadedVideos.splice(index, 1);
    updateVideoList();
}

// Clear all videos
function clearAllVideos() {
    if (confirm('Remove all videos from the list?')) {
        uploadedVideos = [];
        updateVideoList();
    }
}

// Process all videos
async function processAllVideos() {
    if (uploadedVideos.length === 0) {
        alert('No videos to process');
        return;
    }

    const format = document.getElementById('batchFormat').value;
    const processingOption = document.getElementById('batchProcessingOption').value;

    // Show batch processing section
    showSection('batchProgressSection');

    for (let i = 0; i < uploadedVideos.length; i++) {
        const video = uploadedVideos[i];
        video.status = 'processing';
        updateVideoList();

        try {
            await processVideoWithProgress(video, format, processingOption, i);
            video.status = 'completed';
        } catch (error) {
            console.error('Processing failed:', error);
            video.status = 'failed';
        }

        updateVideoList();
        updateBatchProgress(i + 1, uploadedVideos.length);
    }

    showBatchComplete();
}

// Process individual video with progress
async function processVideoWithProgress(videoData, format, option, index) {
    const formData = new FormData();
    formData.append('video', videoData.file);
    formData.append('format', format);

    let endpoint = '/api/convert';
    if (option === 'preset') {
        const preset = document.getElementById('batchPreset').value;
        formData.append('preset', preset);
        endpoint = '/api/preset-style';
    }

    const response = await fetch(endpoint, {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        throw new Error('Processing failed');
    }

    const result = await response.json();
    videoData.jobId = result.job_id;

    // Wait for completion
    await waitForJobCompletion(result.job_id);
}

// Wait for job to complete
async function waitForJobCompletion(jobId) {
    return new Promise((resolve, reject) => {
        const checkInterval = setInterval(async () => {
            try {
                const response = await fetch(`/api/status/${jobId}`);
                const job = await response.json();

                if (job.status === 'completed') {
                    clearInterval(checkInterval);
                    resolve(job);
                } else if (job.status === 'failed') {
                    clearInterval(checkInterval);
                    reject(new Error(job.error));
                }
            } catch (error) {
                clearInterval(checkInterval);
                reject(error);
            }
        }, 2000);
    });
}

// Update batch progress
function updateBatchProgress(completed, total) {
    const progressBar = document.getElementById('batchProgressBar');
    const progressText = document.getElementById('batchProgressText');

    const percentage = (completed / total) * 100;
    progressBar.style.width = percentage + '%';
    progressText.textContent = `Processing: ${completed} of ${total} videos (${Math.round(percentage)}%)`;
}

// Show batch complete
function showBatchComplete() {
    const section = document.getElementById('batchProgressSection');
    section.innerHTML = `
        <div class="batch-complete">
            <h3>✅ All Videos Processed!</h3>
            <p>${uploadedVideos.length} videos have been processed successfully.</p>
            <div class="batch-actions">
                <button onclick="downloadAllVideos()" class="btn btn-success">
                    ⬇️ Download All
                </button>
                <button onclick="resetBatch()" class="btn btn-secondary">
                    🔄 Process More Videos
                </button>
            </div>
        </div>
    `;
}

// Download all processed videos
async function downloadAllVideos() {
    for (const video of uploadedVideos) {
        if (video.jobId && video.status === 'completed') {
            const response = await fetch(`/api/download/${video.jobId}`);
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = video.name.replace(/\.[^/.]+$/, '') + '_processed.mp4';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            // Wait a bit between downloads
            await new Promise(resolve => setTimeout(resolve, 500));
        }
    }
}

// Reset batch processing
function resetBatch() {
    uploadedVideos = [];
    updateVideoList();
    document.getElementById('batchProgressSection').style.display = 'none';
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Create video list container if it doesn't exist
    const mainContainer = document.querySelector('.container');
    if (mainContainer && !document.getElementById('videoListContainer')) {
        const videoListContainer = document.createElement('div');
        videoListContainer.id = 'videoListContainer';
        videoListContainer.className = 'card';
        videoListContainer.style.display = 'none';

        // Insert after the tabs
        const tabs = document.querySelector('.tabs');
        if (tabs && tabs.nextSibling) {
            mainContainer.insertBefore(videoListContainer, tabs.nextSibling);
        } else {
            mainContainer.appendChild(videoListContainer);
        }
    }

    // Create preview modal
    if (!document.getElementById('previewModal')) {
        const modal = document.createElement('div');
        modal.id = 'previewModal';
        modal.className = 'preview-modal';
        modal.innerHTML = `
            <div class="preview-modal-content">
                <div class="preview-header">
                    <h3>Video Preview</h3>
                    <button onclick="closePreview()" class="close-btn">✕</button>
                </div>
                <div class="preview-body">
                    <video id="previewPlayer" controls></video>
                    <div id="previewInfo"></div>
                </div>
                <div class="preview-footer">
                    <button onclick="closePreview()" class="btn btn-secondary">Close</button>
                    <button onclick="processVideoFromPreview()" class="btn btn-primary">
                        ✓ Process This Video
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    // Create batch progress section
    if (!document.getElementById('batchProgressSection')) {
        const section = document.createElement('div');
        section.id = 'batchProgressSection';
        section.className = 'card';
        section.style.display = 'none';
        section.innerHTML = `
            <h3>Processing Videos...</h3>
            <div class="batch-progress-bar">
                <div id="batchProgressBar" class="batch-progress-fill"></div>
            </div>
            <p id="batchProgressText">Starting...</p>
        `;
        mainContainer.appendChild(section);
    }
});

// Process video from preview
function processVideoFromPreview() {
    closePreview();
    const video = uploadedVideos[currentPreviewIndex];
    // Trigger single video processing
    alert('Processing: ' + video.name);
}
