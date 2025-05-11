import React, { useState } from 'react';
import axios from 'axios';

function ImageAnalyzer() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResults(null);
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    
    setLoading(true);
    try {
      const response = await axios.post('/api/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setResults(response.data.results);
    } catch (err) {
      setError('Failed to analyze image: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="image-analyzer">
      <h2>STEGNOX - Advanced Steganography Analysis</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="upload-area">
          <input 
            type="file" 
            accept="image/*" 
            onChange={handleFileChange}
          />
          <button type="submit" disabled={!file || loading}>
            {loading ? 'Analyzing...' : 'Analyze Image'}
          </button>
        </div>
      </form>
      
      {error && <div className="error">{error}</div>}
      
      {results && (
        <div className="results">
          <h3>Analysis Results</h3>
          
          {Object.entries(results).map(([method, result]) => (
            <div key={method} className="result-card">
              <h4>{method.replace('_', ' ')}</h4>
              <pre>{JSON.stringify(result, null, 2)}</pre>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ImageAnalyzer;