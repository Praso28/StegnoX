import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getJob, cancelJob } from '../services/jobService';
import { getImageUrl } from '../services/analysisService';
import AnalysisResults from '../components/AnalysisResults';
import '../styles/JobDetailPage.css';

const JobDetailPage = () => {
  const { jobId } = useParams();
  const navigate = useNavigate();
  
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [refreshInterval, setRefreshInterval] = useState(null);

  const loadJob = async () => {
    try {
      const jobData = await getJob(jobId);
      setJob(jobData);
      
      // If job is still in progress, set up automatic refresh
      if (jobData.status === 'pending' || jobData.status === 'processing') {
        if (!refreshInterval) {
          const interval = setInterval(() => {
            loadJob();
          }, 5000); // Refresh every 5 seconds
          setRefreshInterval(interval);
        }
      } else {
        // Clear interval if job is no longer in progress
        if (refreshInterval) {
          clearInterval(refreshInterval);
          setRefreshInterval(null);
        }
      }
    } catch (err) {
      setError(err.message || 'Failed to load job');
      
      // Clear interval on error
      if (refreshInterval) {
        clearInterval(refreshInterval);
        setRefreshInterval(null);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadJob();
    
    // Clean up interval on unmount
    return () => {
      if (refreshInterval) {
        clearInterval(refreshInterval);
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [jobId]);

  const handleCancelJob = async () => {
    if (window.confirm('Are you sure you want to cancel this job?')) {
      try {
        await cancelJob(jobId);
        loadJob(); // Reload job data
      } catch (err) {
        setError(err.message || 'Failed to cancel job');
      }
    }
  };

  const handleBackToJobs = () => {
    navigate('/jobs');
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  const getStatusClass = (status) => {
    switch (status) {
      case 'pending':
        return 'status-pending';
      case 'processing':
        return 'status-processing';
      case 'completed':
        return 'status-completed';
      case 'failed':
        return 'status-failed';
      case 'cancelled':
        return 'status-cancelled';
      default:
        return '';
    }
  };

  const getPriorityClass = (priority) => {
    switch (priority) {
      case 'high':
        return 'priority-high';
      case 'normal':
        return 'priority-normal';
      case 'low':
        return 'priority-low';
      default:
        return '';
    }
  };

  return (
    <div className="job-detail-page">
      <div className="page-header">
        <button className="back-button" onClick={handleBackToJobs}>
          ← Back to Jobs
        </button>
        <h1>Job Details</h1>
      </div>
      
      {loading ? (
        <div className="loading-message">Loading job details...</div>
      ) : error ? (
        <div className="error-message">{error}</div>
      ) : job ? (
        <div className="job-detail-container">
          <div className="job-info">
            <div className="job-header">
              <h2>Job #{job.job_id}</h2>
              <span className={`job-status ${getStatusClass(job.status)}`}>
                {job.status}
              </span>
            </div>
            
            <div className="job-metadata">
              <div className="metadata-item">
                <span className="metadata-label">Priority:</span>
                <span className={`metadata-value ${getPriorityClass(job.priority)}`}>
                  {job.priority}
                </span>
              </div>
              
              <div className="metadata-item">
                <span className="metadata-label">Created:</span>
                <span className="metadata-value">{formatDate(job.created_at)}</span>
              </div>
              
              {job.started_at && (
                <div className="metadata-item">
                  <span className="metadata-label">Started:</span>
                  <span className="metadata-value">{formatDate(job.started_at)}</span>
                </div>
              )}
              
              {job.completed_at && (
                <div className="metadata-item">
                  <span className="metadata-label">Completed:</span>
                  <span className="metadata-value">{formatDate(job.completed_at)}</span>
                </div>
              )}
              
              {job.worker_id && (
                <div className="metadata-item">
                  <span className="metadata-label">Worker:</span>
                  <span className="metadata-value">{job.worker_id}</span>
                </div>
              )}
            </div>
            
            {job.status === 'pending' && (
              <div className="job-actions">
                <button 
                  className="cancel-button"
                  onClick={handleCancelJob}
                >
                  Cancel Job
                </button>
              </div>
            )}
            
            {job.status === 'processing' && (
              <div className="job-progress">
                <div className="progress-indicator">
                  <div className="progress-spinner"></div>
                  <span>Job is currently processing...</span>
                </div>
                <p>This page will automatically refresh when the job is complete.</p>
              </div>
            )}
            
            {job.status === 'failed' && job.error && (
              <div className="job-error">
                <h3>Error:</h3>
                <p>{job.error}</p>
              </div>
            )}
          </div>
          
          {job.image_path && (
            <div className="job-image">
              <h3>Image</h3>
              <img 
                src={getImageUrl(job.image_path.split('/').pop())} 
                alt="Job" 
                className="job-image-preview"
              />
            </div>
          )}
          
          {job.status === 'completed' && job.results && (
            <div className="job-results">
              <h3>Analysis Results</h3>
              <AnalysisResults results={job.results} />
            </div>
          )}
        </div>
      ) : (
        <div className="not-found">Job not found</div>
      )}
    </div>
  );
};

export default JobDetailPage;
