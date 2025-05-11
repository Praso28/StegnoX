import React from 'react';
import '../styles/Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <h3>StegnoX</h3>
          <p>Advanced Steganography Analysis Tool</p>
        </div>
        
        <div className="footer-section">
          <h3>Links</h3>
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/about">About</a></li>
            <li><a href="/docs">Documentation</a></li>
          </ul>
        </div>
        
        <div className="footer-section">
          <h3>Contact</h3>
          <p>Email: info@stegnox.com</p>
          <p>GitHub: github.com/stegnox</p>
        </div>
      </div>
      
      <div className="footer-bottom">
        <p>&copy; {new Date().getFullYear()} StegnoX. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;
