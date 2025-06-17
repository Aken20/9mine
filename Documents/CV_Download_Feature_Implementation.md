# CV Download Feature Implementation Documentation

## Overview

This document details the implementation of the CV download functionality in our candidate management application. We designed and implemented a streamlined approach for accessing and viewing candidate CVs through both a backend API that serves PDF files directly and a modern frontend interface that displays them in an embedded viewer.

## Backend Implementation

### Changes to `main.py`

#### 1. File Serving with FileResponse

We switched from returning base64-encoded file content to using FastAPI's built-in `FileResponse` for streaming PDF files directly to the client with appropriate headers:

```python
return FileResponse(
    path=cv_file_path,
    filename=os.path.basename(cv_file_path),
    media_type="application/pdf",
    headers={
        "Content-Disposition": f"inline; filename=\"CV_{candidate.get('name', 'candidate')}.pdf\"",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "SAMEORIGIN",
        "Access-Control-Allow-Origin": "*",
        "Cache-Control": "max-age=3600"
    }
)
```

#### 2. Robust Path Resolution

We implemented a comprehensive path resolution function that attempts to locate CV files across multiple potential locations:

```python
def resolve_cv_path(cv_path, candidate_name=None):
    import os
    
    # These are the possible locations to check for CV files
    possible_paths = []
    
    # Get the base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add the original path
    if not os.path.isabs(cv_path):
        possible_paths.append(os.path.join(base_dir, cv_path))
    else:
        possible_paths.append(cv_path)
        
    # Try the extracted directory structure
    filename = os.path.basename(cv_path)
    
    # Docker container paths
    possible_paths.append("/app/media/CVs To Share June 2024/" + filename)
    
    # Check various locations
    possible_paths.append(os.path.join(base_dir, "media", "CVs To Share June 2024", filename))
    possible_paths.append(os.path.join(base_dir, "media", filename))
    possible_paths.append(os.path.join("/app/media", filename))
    
    # Try to find by candidate name
    if candidate_name:
        candidate_name_clean = candidate_name.replace(" ", "_")
        possible_paths.append(f"/app/media/CVs To Share June 2024/{candidate_name_clean}_CV.pdf")
        possible_paths.append(f"/app/media/CVs To Share June 2024/{candidate_name_clean.split('_')[0]}_CV.pdf")
    
    # Check all paths
    for path in possible_paths:
        if os.path.exists(path):
            return path
            
    # No valid path found
    return None
```

#### 3. Fix for Syntax Error

We removed a nested `try` block that was causing a syntax error in the `download_cv` function:

```python
# Before (problematic):
try:
    # Outer try block code...
    try:
        # Inner try block code...
    # Missing except clause here
    
# After (fixed):
try:
    # Outer try block code...
    # Direct code without unnecessary nested try...
except HTTPException as e:
    # Exception handling...
```

#### 4. Authentication and Error Handling

The API now performs proper token validation and returns meaningful error messages for various edge cases:

- Invalid or expired tokens
- Missing candidate IDs
- Candidates not found in the database
- Missing or inaccessible CV files

## Frontend Implementation

### Changes to `SearchResults.jsx`

#### 1. Modal PDF Viewer

Implemented a modern, interactive modal for displaying PDFs inline instead of forcing downloads:

```jsx
// Create a modal for PDF preview
const modal = document.createElement('div');
modal.style.position = 'fixed';
modal.style.top = '0';
modal.style.left = '0';
modal.style.width = '100%';
modal.style.height = '100%';
modal.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
modal.style.zIndex = '1500';
modal.style.display = 'flex';
modal.style.flexDirection = 'column';
modal.style.alignItems = 'center';
modal.style.justifyContent = 'center';
```

#### 2. Interactive Controls

Added title bar with download and close options:

```jsx
// Title
const modalTitle = document.createElement('div');
modalTitle.textContent = `${candidate.name}'s CV`;
modalTitle.style.fontWeight = 'bold';
modalTitle.style.color = '#034C53';

// Download button
const downloadButton = document.createElement('button');
downloadButton.textContent = 'Download';
downloadButton.style.backgroundColor = '#034C53';
downloadButton.style.color = 'white';
// ... (styling)

// Close button
const closeButton = document.createElement('button');
closeButton.textContent = '×';
closeButton.style.background = 'none';
// ... (styling)
```

#### 3. PDF Display via iframe

Used an iframe for native browser rendering of PDFs:

```jsx
// Create iframe for PDF
const iframe = document.createElement('iframe');
iframe.style.width = '90%';
iframe.style.height = '85%';
iframe.style.border = 'none';
iframe.style.backgroundColor = 'white';

// Set the iframe source to the blob URL
iframe.src = blobUrl;
```

#### 4. Direct Binary Processing

Changed from base64 decoding to direct blob handling:

```jsx
// Create a blob URL directly from the response
const blob = await response.blob();
const blobUrl = URL.createObjectURL(blob);
```

#### 5. Enhanced Error Handling

Added comprehensive error handling with visual feedback:

```jsx
try {
    // Main functionality
} catch (error) {
    console.error('Error in handleDownloadCV:', error);
    
    // Show error in the iframe
    const existingIframe = document.querySelector('iframe');
    if (existingIframe) {
        existingIframe.style.padding = '20px';
        existingIframe.style.backgroundColor = '#f8d7da';
        existingIframe.srcdoc = `<div style="color:#721c24; padding:20px; text-align:center;">
            <h3>Error Loading PDF</h3>
            <p>${error.message}</p>
        </div>`;
    }
    
    // Visual error feedback
    if (document.body.contains(downloadDiv)) {
        downloadDiv.style.backgroundColor = '#F44336';
        downloadDiv.textContent = `Error loading CV: ${error.message}`;
        // ... (cleanup code)
    }
}
```

## Technical Benefits

1. **Performance**: Direct file streaming is more efficient than base64 encoding
2. **User Experience**: In-app PDF viewing without leaving the application
3. **Compatibility**: Works across all major browsers with native PDF support
4. **Flexibility**: Both viewing and downloading are supported

## Security Considerations

1. **Authentication**: Token validation ensures only authorized users can access CVs
2. **Headers**: Security headers prevent common web vulnerabilities
3. **Resource Cleanup**: All blob URLs are properly revoked to prevent memory leaks

## Deployment Notes

After implementing these changes, the application should be restarted using:

```bash
docker restart backend
```

This will ensure the backend properly serves the PDF files with the new implementation.
