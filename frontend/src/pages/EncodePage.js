import React, { useState } from 'react';
import FileUpload from '../components/FileUpload';
import { encodeMessage, getImageUrl } from '../services/analysisService';
import '../styles/EncodePage.css';

const EncodePage = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [method, setMethod] = useState('lsb_encoding');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  const handleFileSelect = (selectedFile) => {
    setFile(selectedFile);
    setError('');
    setResult(null);
  };

  const handleMethodChange = (e) => {
    setMethod(e.target.value);
  };

  const handleMessageChange = (e) => {
    setMessage(e.target.value);
  };

  const handleEncode = async () => {
    if (!file) {
      setError('Please select an image');
      return;
    }
    
    if (!message) {
      setError('Please enter a message to encode');
      return;
    }
    
    setError('');
    setLoading(true);
    
    try {
      const encodingResult = await encodeMessage(file, message, method);
      setResult(encodingResult);
    } catch (err) {
      setError(err.message || 'Encoding failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (result && result.filename) {
      const imageUrl = getImageUrl(result.filename);
      
      // Create a temporary link element
      const link = document.createElement('a');
      link.href = imageUrl;
      link.download = result.filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  return (
    <div className="encode-page">
      <div className="page-header">
        <h1>Encode Message</h1>
        <p>Hide a secret message in an image</p>
      </div>
      
      <div className="encode-container">
        <div className="encode-options">
          <div className="option-group">
            <label htmlFor="method" className="option-label">Encoding Method</label>
            <select
              id="method"
              value={method}
              onChange={handleMethodChange}
              disabled={loading}
              className="option-select"
            >
              <option value="lsb_encoding">LSB Encoding</option>
              <option value="parity_bit_encoding">Parity Bit Encoding</option>
              <option value="metadata_encoding">Metadata Encoding</option>
            </select>
            
            <div className="method-info">
              {method === 'lsb_encoding' && (
                <p>LSB Encoding hides data in the least significant bits of pixel values. It's the most common steganography method.</p>
              )}
              {method === 'parity_bit_encoding' && (
                <p>Parity Bit Encoding modifies pixel values to achieve desired parity based on message bits.</p>
              )}
              {method === 'metadata_encoding' && (
                <p>Metadata Encoding hides data in the image's metadata fields, which is less secure but easier to implement.</p>
              )}
            </div>
          </div>
          
          <div className="option-group">
            <label htmlFor="message" className="option-label">Message</label>
            <textarea
              id="message"
              value={message}
              onChange={handleMessageChange}
              disabled={loading}
              placeholder="Enter your secret message here..."
              className="message-input"
              rows={6}
            />
            <div className="message-counter">
              {message.length} characters
            </div>
          </div>
        </div>
        
        <div className="file-upload-section">
          <h3>Cover Image</h3>
          <FileUpload onFileSelect={handleFileSelect} />
          
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}
          
          <button 
            className="encode-button"
            onClick={handleEncode}
            disabled={!file || !message || loading}
          >
            {loading ? 'Encoding...' : 'Encode Message'}
          </button>
        </div>
        
        {result && (
          <div className="result-section">
            <h2>Encoding Successful!</h2>
            <p>{result.message}</p>
            
            <div className="result-image">
              <h3>Encoded Image</h3>
              <img 
                src={getImageUrl(result.filename)} 
                alt="Encoded" 
                className="encoded-image"
              />
              
              <button 
                className="download-button"
                onClick={handleDownload}
              >
                Download Encoded Image
              </button>
            </div>
            
            <div className="security-note">
              <h3>Security Note</h3>
              <p>
                The encoded image has been saved on the server. For maximum security,
                download the image and delete it from your account when you're done.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default EncodePage;
