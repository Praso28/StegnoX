import React, { useState, useRef } from 'react';
import '../styles/FileUpload.css';

const FileUpload = ({ onFileSelect, accept = "image/*", maxSize = 16 * 1024 * 1024 }) => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    processFile(selectedFile);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const selectedFile = e.dataTransfer.files[0];
      processFile(selectedFile);
    }
  };

  const processFile = (selectedFile) => {
    // Reset state
    setError(null);
    
    // Validate file
    if (!selectedFile) {
      return;
    }
    
    // Check file size
    if (selectedFile.size > maxSize) {
      setError(`File size exceeds the maximum limit of ${maxSize / (1024 * 1024)}MB`);
      return;
    }
    
    // Check file type
    const fileType = selectedFile.type;
    if (!fileType.startsWith('image/')) {
      setError('Only image files are allowed');
      return;
    }
    
    // Create preview
    const reader = new FileReader();
    reader.onload = () => {
      setPreview(reader.result);
    };
    reader.readAsDataURL(selectedFile);
    
    // Set file and call parent handler
    setFile(selectedFile);
    onFileSelect(selectedFile);
  };

  const handleClick = () => {
    fileInputRef.current.click();
  };

  const handleRemove = () => {
    setFile(null);
    setPreview(null);
    setError(null);
    onFileSelect(null);
    
    // Reset file input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="file-upload">
      <div 
        className={`upload-area ${isDragging ? 'dragging' : ''} ${file ? 'has-file' : ''}`}
        onClick={!file ? handleClick : undefined}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input 
          type="file" 
          ref={fileInputRef}
          onChange={handleFileChange}
          accept={accept}
          className="file-input"
        />
        
        {!file && (
          <div className="upload-prompt">
            <i className="upload-icon">📁</i>
            <p>Drag and drop an image here, or click to select</p>
            <span className="upload-hint">Supported formats: JPG, PNG, GIF, BMP</span>
          </div>
        )}
        
        {file && preview && (
          <div className="file-preview">
            <img src={preview} alt="Preview" className="preview-image" />
            <div className="file-info">
              <p className="file-name">{file.name}</p>
              <p className="file-size">{(file.size / 1024).toFixed(2)} KB</p>
            </div>
            <button className="remove-button" onClick={handleRemove}>
              Remove
            </button>
          </div>
        )}
      </div>
      
      {error && (
        <div className="upload-error">
          {error}
        </div>
      )}
    </div>
  );
};

export default FileUpload;
