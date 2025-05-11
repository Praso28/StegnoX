import React, { useState, useEffect } from 'react';
import JobList from '../components/JobList';
import { getJobs, cancelJob } from '../services/jobService';
import '../styles/JobsPage.css';

const JobsPage = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const limit = 10;

  const loadJobs = async (reset = false) => {
    try {
      setLoading(true);
      const newPage = reset ? 0 : page;
      const offset = newPage * limit;
      
      const fetchedJobs = await getJobs(statusFilter || null, limit, offset);
      
      if (reset) {
        setJobs(fetchedJobs);
        setPage(0);
      } else {
        setJobs([...jobs, ...fetchedJobs]);
        setPage(newPage + 1);
      }
      
      // Check if there are more jobs to load
      setHasMore(fetchedJobs.length === limit);
    } catch (err) {
      setError(err.message || 'Failed to load jobs');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadJobs(true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [statusFilter]);

  const handleStatusFilterChange = (e) => {
    setStatusFilter(e.target.value);
  };

  const handleCancelJob = async (jobId) => {
    try {
      await cancelJob(jobId);
      
      // Update the job in the list
      setJobs(jobs.map(job => 
        job.job_id === jobId 
          ? { ...job, status: 'cancelled' } 
          : job
      ));
    } catch (err) {
      setError(err.message || 'Failed to cancel job');
    }
  };

  const handleLoadMore = () => {
    loadJobs();
  };

  return (
    <div className="jobs-page">
      <div className="page-header">
        <h1>Jobs</h1>
        <p>Manage your steganography analysis jobs</p>
      </div>
      
      <div className="jobs-container">
        <div className="jobs-filters">
          <div className="filter-group">
            <label htmlFor="statusFilter" className="filter-label">Status</label>
            <select
              id="statusFilter"
              value={statusFilter}
              onChange={handleStatusFilterChange}
              className="filter-select"
            >
              <option value="">All</option>
              <option value="pending">Pending</option>
              <option value="processing">Processing</option>
              <option value="completed">Completed</option>
              <option value="failed">Failed</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>
        </div>
        
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}
        
        <div className="jobs-list-container">
          {loading && jobs.length === 0 ? (
            <div className="loading-message">Loading jobs...</div>
          ) : jobs.length === 0 ? (
            <div className="no-jobs-message">
              No jobs found. 
              {statusFilter && ' Try changing the status filter.'}
            </div>
          ) : (
            <>
              <JobList jobs={jobs} onCancelJob={handleCancelJob} />
              
              {hasMore && (
                <div className="load-more">
                  <button 
                    className="load-more-button"
                    onClick={handleLoadMore}
                    disabled={loading}
                  >
                    {loading ? 'Loading...' : 'Load More'}
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default JobsPage;
