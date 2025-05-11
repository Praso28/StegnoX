import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/JobList.css';

const JobList = ({ jobs, onCancelJob }) => {
  if (!jobs || jobs.length === 0) {
    return <div className="no-jobs">No jobs found</div>;
  }

  const formatDate = (dateString) => {
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

  const handleCancel = (e, jobId) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (window.confirm('Are you sure you want to cancel this job?')) {
      onCancelJob(jobId);
    }
  };

  return (
    <div className="job-list">
      <table className="jobs-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Status</th>
            <th>Priority</th>
            <th>Created</th>
            <th>Updated</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {jobs.map((job) => (
            <tr key={job.job_id} className="job-row">
              <td>
                <Link to={`/jobs/${job.job_id}`} className="job-id">
                  {job.job_id.substring(0, 8)}...
                </Link>
              </td>
              <td>
                <span className={`job-status ${getStatusClass(job.status)}`}>
                  {job.status}
                </span>
              </td>
              <td>
                <span className={`job-priority ${getPriorityClass(job.priority)}`}>
                  {job.priority}
                </span>
              </td>
              <td>{formatDate(job.created_at)}</td>
              <td>{formatDate(job.updated_at)}</td>
              <td className="job-actions">
                <Link to={`/jobs/${job.job_id}`} className="view-button">
                  View
                </Link>
                
                {job.status === 'pending' && (
                  <button 
                    className="cancel-button"
                    onClick={(e) => handleCancel(e, job.job_id)}
                  >
                    Cancel
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default JobList;
