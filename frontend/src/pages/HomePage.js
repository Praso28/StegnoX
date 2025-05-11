import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/HomePage.css';

const HomePage = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div className="home-page">
      <section className="hero">
        <div className="hero-content">
          <h1>StegnoX</h1>
          <h2>Advanced Steganography Analysis Tool</h2>
          <p>
            Detect and analyze hidden data in images with our powerful steganography tools.
            StegnoX provides state-of-the-art algorithms for detecting and extracting hidden messages.
          </p>
          
          {isAuthenticated ? (
            <div className="hero-buttons">
              <Link to="/analyze" className="primary-button">Analyze Image</Link>
              <Link to="/encode" className="secondary-button">Encode Message</Link>
            </div>
          ) : (
            <div className="hero-buttons">
              <Link to="/register" className="primary-button">Get Started</Link>
              <Link to="/login" className="secondary-button">Login</Link>
            </div>
          )}
        </div>
      </section>
      
      <section className="features">
        <h2>Features</h2>
        
        <div className="feature-grid">
          <div className="feature-card">
            <div className="feature-icon">🔍</div>
            <h3>Advanced Detection</h3>
            <p>
              Detect hidden data using multiple algorithms including LSB, 
              parity bit analysis, DCT analysis, and more.
            </p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">🔐</div>
            <h3>Secure Encoding</h3>
            <p>
              Hide your messages securely in images using various 
              steganography techniques.
            </p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Detailed Analysis</h3>
            <p>
              Get comprehensive analysis results with visualizations 
              and confidence scores.
            </p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">⚙️</div>
            <h3>Job Management</h3>
            <p>
              Queue and manage multiple analysis jobs with different 
              priorities.
            </p>
          </div>
        </div>
      </section>
      
      <section className="how-it-works">
        <h2>How It Works</h2>
        
        <div className="steps">
          <div className="step">
            <div className="step-number">1</div>
            <h3>Upload Image</h3>
            <p>Upload the image you want to analyze or use as a cover for your message.</p>
          </div>
          
          <div className="step">
            <div className="step-number">2</div>
            <h3>Select Operation</h3>
            <p>Choose to analyze the image for hidden data or encode your own message.</p>
          </div>
          
          <div className="step">
            <div className="step-number">3</div>
            <h3>Process</h3>
            <p>Our advanced algorithms will process your request in the background.</p>
          </div>
          
          <div className="step">
            <div className="step-number">4</div>
            <h3>View Results</h3>
            <p>Get detailed results and visualizations of the analysis or your encoded image.</p>
          </div>
        </div>
      </section>
      
      <section className="cta">
        <h2>Ready to Get Started?</h2>
        <p>Join StegnoX today and discover the hidden world of steganography.</p>
        
        {isAuthenticated ? (
          <Link to="/dashboard" className="cta-button">Go to Dashboard</Link>
        ) : (
          <Link to="/register" className="cta-button">Create Account</Link>
        )}
      </section>
    </div>
  );
};

export default HomePage;
