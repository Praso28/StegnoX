import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import FileUpload from '../components/FileUpload';
import AnalysisResults from '../components/AnalysisResults';
import { analyzeImage } from '../services/analysisService';
import { createJob } from '../services/jobService';
import '../styles/AnalyzePage.css';

const AnalyzePage = () => {
  const [file, setFile] = useState(null);
  const [methods, setMethods] = useState('all');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [jobMode, setJobMode] = useState(false);
  const [priority, setPriority] = useState('normal');
  const [jobCreated, setJobCreated] = useState(false);
  const [jobId, setJobId] = useState('');
  
  const navigate = useNavigate();

  const handleFileSelect = (selectedFile) => {
    setFile(selectedFile);
    setResults(null);
    setError('');
    setJobCreated(false);
  };

  const handleMethodChange = (e) => {
    setMethods(e.target.value);
  };

  const handleModeChange = (e) => {
    setJobMode(e.target.checked);
  };

  const handlePriorityChange = (e) => {
    setPriority(e.target.value);
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please select an image to analyze');
      return;
    }
    
    setError('');
    setLoading(true);
    
    try {
      if (jobMode) {
        // Create a job
        const job = await createJob(file, priority);
        setJobId(job.job_id);
        setJobCreated(true);
      } else {
        // Analyze directly
        const analysisResults = await analyzeImage(file, methods);
        setResults(analysisResults);
      }
    } catch (err) {
      setError(err.message || 'Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleViewJob = () => {
    navigate(`/jobs/${jobId}`);
  };

  return (
    <div className="analyze-page">
      <div className="page-header">
        <h1>Analyze Image</h1>
        <p>Upload an image to analyze for hidden data</p>
      </div>
      
      <div className="analyze-container">
        <div className="analyze-options">
          <div className="option-group">
            <label className="option-label">Analysis Mode</label>
            <div className="toggle-switch">
              <input
                type="checkbox"
                id="jobMode"
                checked={jobMode}
                onChange={handleModeChange}
                disabled={loading}
              />
              <label htmlFor="jobMode">
                <span className="toggle-label">Direct</span>
                <span className="toggle-handle"></span>
                <span className="toggle-label">Job Queue</span>
              </label>
            </div>
            <p className="option-help">
              {jobMode 
                ? 'Job Queue: Process in the background and view results later' 
                : 'Direct: Process immediately and view results now'}
            </p>
          </div>
          
          {jobMode && (
            <div className="option-group">
              <label htmlFor="priority" className="option-label">Job Priority</label>
              <select
                id="priority"
                value={priority}
                onChange={handlePriorityChange}
                disabled={loading}
                className="option-select"
              >
                <option value="low">Low</option>
                <option value="normal">Normal</option>
                <option value="high">High</option>
              </select>
            </div>
          )}
          
          <div className="option-group">
            <label htmlFor="methods" className="option-label">Analysis Methods</label>
            <select
              id="methods"
              value={methods}
              onChange={handleMethodChange}
              disabled={loading}
              className="option-select"
            >
              <option value="all">All Methods</option>
              <option value="lsb_extraction">LSB Extraction</option>
              <option value="parity_bit_extraction">Parity Bit Extraction</option>
              <option value="metadata_extraction">Metadata Extraction</option>
              <option value="dct_analysis">DCT Analysis</option>
              <option value="bit_plane_analysis">Bit Plane Analysis</option>
              <option value="histogram_analysis">Histogram Analysis</option>
            </select>
          </div>
        </div>
        
        <div className="file-upload-section">
          <FileUpload onFileSelect={handleFileSelect} />
          
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}
          
          <button 
            className="analyze-button"
            onClick={handleAnalyze}
            disabled={!file || loading}
          >
            {loading 
              ? (jobMode ? 'Creating Job...' : 'Analyzing...') 
              : (jobMode ? 'Create Analysis Job' : 'Analyze Image')}
          </button>
        </div>
        
        {jobCreated && (
          <div className="job-created">
            <h3>Job Created Successfully!</h3>
            <p>Your analysis job has been created and is now in the queue.</p>
            <p>Job ID: <span className="job-id">{jobId}</span></p>
            <button 
              className="view-job-button"
              onClick={handleViewJob}
            >
              View Job Status
            </button>
          </div>
        )}
        
        {results && (
          <div className="results-section">
            <h2>Analysis Results</h2>
            <AnalysisResults results={results} />
          </div>
        )}
      </div>
    </div>
  );
};

export default AnalyzePage;
