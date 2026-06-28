/**
 * Project Aura - Upload Handler JavaScript
 * Manages file selection, upload, and user interactions
 */

// Global state
let selectedFiles = [];

/**
 * Initialize upload handler
 */
function initializeUploadHandler() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const clearBtn = document.getElementById('clearBtn');
    const uploadMoreBtn = document.getElementById('uploadMoreBtn');

    if (!uploadArea || !fileInput) {
        console.error('Upload area or file input not found');
        return;
    }

    // Click to browse
    uploadArea.addEventListener('click', () => fileInput.click());

    // File input change
    fileInput.addEventListener('change', handleFileSelection);

    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);

    // Upload button
    if (uploadBtn) {
        uploadBtn.addEventListener('click', handleUpload);
    }

    // Clear button
    if (clearBtn) {
        clearBtn.addEventListener('click', clearFileSelection);
    }

    // Upload more button
    if (uploadMoreBtn) {
        uploadMoreBtn.addEventListener('click', function() {
            document.getElementById('resultsSection').style.display = 'none';
            document.getElementById('uploadForm').style.display = 'block';
            selectedFiles = [];
            updateFilesList();
        });
    }
}

/**
 * Handle file selection from input
 */
function handleFileSelection(e) {
    const files = e.target.files;
    selectedFiles = Array.from(files);
    updateFilesList();
}

/**
 * Handle drag over event
 */
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('uploadArea').classList.add('drag-over');
}

/**
 * Handle drag leave event
 */
function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('uploadArea').classList.remove('drag-over');
}

/**
 * Handle drop event
 */
function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('uploadArea').classList.remove('drag-over');

    const files = e.dataTransfer.files;
    selectedFiles = Array.from(files);
    updateFilesList();
}

/**
 * Update files list display
 */
function updateFilesList() {
    const filesList = document.getElementById('filesList');
    const filesContainer = document.getElementById('filesContainer');
    const uploadBtn = document.getElementById('uploadBtn');
    const clearBtn = document.getElementById('clearBtn');

    if (selectedFiles.length === 0) {
        filesList.style.display = 'none';
        uploadBtn.style.display = 'none';
        clearBtn.style.display = 'none';
        return;
    }

    // Show files list
    filesList.style.display = 'block';
    uploadBtn.style.display = 'inline-block';
    uploadBtn.disabled = false;
    clearBtn.style.display = 'inline-block';

    // Clear and rebuild files list
    filesContainer.innerHTML = '';

    selectedFiles.forEach((file, index) => {
        const fileItem = createFileItem(file, index);
        filesContainer.appendChild(fileItem);
    });
}

/**
 * Create file item element
 */
function createFileItem(file, index) {
    const div = document.createElement('div');
    div.className = 'file-item';

    const icon = getFileIcon(file.name);
    const size = formatFileSize(file.size);

    div.innerHTML = `
        <i class="fas ${icon}"></i>
        <div class="file-info">
            <div class="file-name">${escapeHtml(file.name)}</div>
            <div class="file-size">${size}</div>
        </div>
        <button type="button" class="file-remove" data-index="${index}">
            <i class="fas fa-trash"></i>
        </button>
    `;

    // Remove button handler
    div.querySelector('.file-remove').addEventListener('click', () => {
        selectedFiles.splice(index, 1);
        updateFilesList();
    });

    return div;
}

/**
 * Get file icon based on extension
 */
function getFileIcon(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    switch (ext) {
        case 'pdf':
            return 'fa-file-pdf text-danger';
        case 'docx':
            return 'fa-file-word text-primary';
        case 'pptx':
            return 'fa-file-powerpoint text-warning';
        default:
            return 'fa-file text-secondary';
    }
}

/**
 * Format file size for display
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Clear file selection
 */
function clearFileSelection() {
    selectedFiles = [];
    document.getElementById('fileInput').value = '';
    updateFilesList();
}

/**
 * Handle file upload
 */
function handleUpload() {
    if (selectedFiles.length === 0) {
        showError('Please select at least one file to upload');
        return;
    }

    // Show progress
    document.getElementById('uploadProgress').style.display = 'block';
    document.getElementById('uploadBtn').disabled = true;
    document.getElementById('clearBtn').disabled = true;

    // Create form data
    const formData = new FormData();
    selectedFiles.forEach(file => {
        formData.append('files', file);
    });

    // Upload files
    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        handleUploadResponse(data);
    })
    .catch(error => {
        console.error('Upload error:', error);
        document.getElementById('uploadProgress').style.display = 'none';
        document.getElementById('uploadBtn').disabled = false;
        document.getElementById('clearBtn').disabled = false;
        showError('Upload failed. Please try again.');
    });
}

/**
 * Handle upload response
 */
function handleUploadResponse(data) {
    const uploadProgress = document.getElementById('uploadProgress');
    const uploadBtn = document.getElementById('uploadBtn');
    const clearBtn = document.getElementById('clearBtn');
    const resultsSection = document.getElementById('resultsSection');
    const successMessage = document.getElementById('successMessage');
    const documentsInfo = document.getElementById('documentsInfo');

    uploadProgress.style.display = 'none';
    uploadBtn.disabled = false;
    clearBtn.disabled = false;

    if (data.success) {
        try {
            // Show success message
            successMessage.innerHTML = `
                <i class="fas fa-check-circle"></i>
                <strong>Success!</strong> ${data.processed} document(s) uploaded and processed successfully.
                ${data.errors && data.errors.length > 0 ?
                    `<p class="mt-2"><small>${data.failed} file(s) failed to process.</small></p>` :
                    ''}
            `;

            // Show documents info
            documentsInfo.innerHTML = `
                <h6 class="mb-3">Processed Documents:</h6>
                <div class="row">
                    ${data.results.map(result => `
                        <div class="col-md-6 mb-3">
                            <div class="card border-success">
                                <div class="card-body">
                                    <h6 class="card-title">
                                        <i class="fas ${getFileIcon(result.filename)}"></i>
                                        ${escapeHtml(result.filename)}
                                    </h6>
                                    <p class="card-text text-muted small">
                                        <strong>Type:</strong> ${result.extension.toUpperCase()}<br>
                                        <strong>Pages:</strong> ${result.page_count}<br>
                                        <strong>Tables:</strong> ${result.has_tables ? 'Yes' : 'No'}
                                    </p>
                                    <p class="card-text">
                                        <strong>Preview:</strong><br>
                                        <small>${escapeHtml(result.preview)}</small>
                                    </p>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;

            // Show errors if any
            if (data.errors && data.errors.length > 0) {
                const errorHtml = `
                    <div class="alert alert-warning mt-3">
                        <strong>Failed Files:</strong>
                        <ul class="mb-0 mt-2">
                            ${data.errors.map(error => `<li>${escapeHtml(error)}</li>`).join('')}
                        </ul>
                    </div>
                `;
                documentsInfo.innerHTML += errorHtml;
            }

            // Hide upload form and show results
            const uploadForm = document.getElementById('uploadForm');
            const filesList = document.getElementById('filesList');

            if (uploadForm) uploadForm.style.display = 'none';
            if (filesList) filesList.style.display = 'none';

            if (resultsSection) {
                resultsSection.style.display = 'block';
                console.log('Results section displayed successfully');
            } else {
                console.error('Results section element not found!');
                showError('Could not display results. Please refresh and try again.');
            }

            // Clear file selection
            selectedFiles = [];
            document.getElementById('fileInput').value = '';

        } catch (error) {
            console.error('Error in handleUploadResponse:', error);
            showError('An error occurred while processing the response. Please try again.');
        }

    } else {
        // Show error
        const errorMsg = data.error || 'Upload failed. Please try again.';
        if (data.errors && data.errors.length > 0) {
            showErrorList(data.errors);
        } else {
            showError(errorMsg);
        }
    }
}

/**
 * Show error message
 */
function showError(message) {
    const uploadForm = document.getElementById('uploadForm');
    const existingAlert = uploadForm.querySelector('.alert');
    
    if (existingAlert) {
        existingAlert.remove();
    }

    const alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-dismissible fade show';
    alert.innerHTML = `
        <i class="fas fa-exclamation-circle"></i>
        <strong>Error:</strong> ${escapeHtml(message)}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    uploadForm.parentElement.insertBefore(alert, uploadForm);
}

/**
 * Show error list
 */
function showErrorList(errors) {
    const uploadForm = document.getElementById('uploadForm');
    const existingAlert = uploadForm.querySelector('.alert');
    
    if (existingAlert) {
        existingAlert.remove();
    }

    const alert = document.createElement('div');
    alert.className = 'alert alert-warning alert-dismissible fade show';
    alert.innerHTML = `
        <i class="fas fa-exclamation-triangle"></i>
        <strong>Some files failed to process:</strong>
        <ul class="mb-0 mt-2">
            ${errors.map(error => `<li>${escapeHtml(error)}</li>`).join('')}
        </ul>
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    uploadForm.parentElement.insertBefore(alert, uploadForm);
}

/**
 * Escape HTML special characters
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
