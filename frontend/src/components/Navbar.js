import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/Navbar.css';

const Navbar = () => {
  const { isAuthenticated, currentUser, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/">
          <h1>StegnoX</h1>
        </Link>
      </div>
      
      <div className="navbar-menu">
        <ul className="navbar-nav">
          <li className="nav-item">
            <Link to="/" className="nav-link">Home</Link>
          </li>
          
          {isAuthenticated ? (
            <>
              <li className="nav-item">
                <Link to="/dashboard" className="nav-link">Dashboard</Link>
              </li>
              <li className="nav-item">
                <Link to="/analyze" className="nav-link">Analyze</Link>
              </li>
              <li className="nav-item">
                <Link to="/encode" className="nav-link">Encode</Link>
              </li>
              <li className="nav-item">
                <Link to="/jobs" className="nav-link">Jobs</Link>
              </li>
            </>
          ) : (
            <li className="nav-item">
              <Link to="/about" className="nav-link">About</Link>
            </li>
          )}
        </ul>
      </div>
      
      <div className="navbar-auth">
        {isAuthenticated ? (
          <div className="user-menu">
            <Link to="/profile" className="profile-link">
              {currentUser?.username || 'Profile'}
            </Link>
            <button onClick={handleLogout} className="logout-button">
              Logout
            </button>
          </div>
        ) : (
          <div className="auth-buttons">
            <Link to="/login" className="login-button">Login</Link>
            <Link to="/register" className="register-button">Register</Link>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
