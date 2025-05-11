import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getJobs } from '../services/jobService';
import JobList from '../components/JobList';
import '../styles/DashboardPage.css';

const DashboardPage = () => {
  const { currentUser } = useAuth();
  const [recentJobs, setRecentJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchRecentJobs = async () => {
      try {
        const jobs = await getJobs(null, 5, 0);
        setRecentJobs(jobs);
      } catch (err) {
        setError('Failed to load recent jobs');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchRecentJobs();
  }, []);

  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <p>Welcome back, {currentUser?.username || 'User'}!</p>
      </div>
      
      <div className="dashboard-grid">
        <div className="dashboard-card quick-actions">
          <h2>Quick Actions</h2>
          <div className="action-buttons">
            <Link to="/analyze" className="action-button analyze">
              <span className="action-icon">🔍</span>
              <span className="action-text">Analyze Image</span>
            </Link>
            
            <Link to="/encode" className="action-button encode">
              <span className="action-icon">🔐</span>
              <span className="action-text">Encode Message</span>
            </Link>
            
            <Link to="/jobs" className="action-button jobs">
              <span className="action-icon">📋</span>
              <span className="action-text">View All Jobs</span>
            </Link>
            
            <Link to="/profile" className="action-button profile">
              <span className="action-icon">👤</span>
              <span className="action-text">Profile Settings</span>
            </Link>
          </div>
        </div>
        
        <div className="dashboard-card recent-jobs">
          <h2>Recent Jobs</h2>
          
          {loading ? (
            <div className="loading">Loading recent jobs...</div>
          ) : error ? (
            <div className="error">{error}</div>
          ) : (
            <>
              <JobList jobs={recentJobs} />
              
              <div className="view-all">
                <Link to="/jobs" className="view-all-link">
                  View All Jobs
                </Link>
              </div>
            </>
          )}
        </div>
        
        <div className="dashboard-card stats">
          <h2>Statistics</h2>
          
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-value">{recentJobs.length}</div>
              <div className="stat-label">Recent Jobs</div>
            </div>
            
            <div className="stat-item">
              <div className="stat-value">
                {recentJobs.filter(job => job.status === 'completed').length}
              </div>
              <div className="stat-label">Completed</div>
            </div>
            
            <div className="stat-item">
              <div className="stat-value">
                {recentJobs.filter(job => job.status === 'pending' || job.status === 'processing').length}
              </div>
              <div className="stat-label">In Progress</div>
            </div>
            
            <div className="stat-item">
              <div className="stat-value">
                {recentJobs.filter(job => job.status === 'failed').length}
              </div>
              <div className="stat-label">Failed</div>
            </div>
          </div>
        </div>
        
        <div className="dashboard-card help">
          <h2>Help & Resources</h2>
          
          <div className="help-links">
            <a href="/docs" className="help-link">
              <span className="help-icon">📚</span>
              <span className="help-text">Documentation</span>
            </a>
            
            <a href="/faq" className="help-link">
              <span className="help-icon">❓</span>
              <span className="help-text">FAQ</span>
            </a>
            
            <a href="/support" className="help-link">
              <span className="help-icon">🛟</span>
              <span className="help-text">Support</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
