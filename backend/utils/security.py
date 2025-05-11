"""
Security utilities for StegnoX backend
"""

from flask import request, current_app

def add_security_headers(response):
    """
    Add security headers to the response
    
    Args:
        response: Flask response object
        
    Returns:
        response: Modified response object
    """
    # Content Security Policy
    response.headers['Content-Security-Policy'] = "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'"
    
    # Prevent MIME type sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Prevent clickjacking
    response.headers['X-Frame-Options'] = 'DENY'
    
    # Enable XSS protection
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Strict Transport Security (only in production)
    if not current_app.debug and not current_app.testing:
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # Referrer Policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Feature Policy
    response.headers['Feature-Policy'] = "camera 'none'; microphone 'none'; geolocation 'none'"
    
    # Cache Control (for sensitive pages)
    if request.path.startswith('/api/v1/auth'):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    
    return response

def configure_cors(app):
    """
    Configure CORS for the application
    
    Args:
        app: Flask application
    """
    # Import CORS here to make it optional
    try:
        from flask_cors import CORS
        
        # Configure CORS
        CORS(app, resources={
            r"/api/*": {
                "origins": current_app.config.get('CORS_ORIGINS', '*'),
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "expose_headers": ["Content-Type", "X-Total-Count"],
                "supports_credentials": True,
                "max_age": 600
            }
        })
    except ImportError:
        app.logger.warning("flask-cors not installed. CORS not configured.")

def init_security(app):
    """
    Initialize security features for the application
    
    Args:
        app: Flask application
    """
    # Add security headers to all responses
    app.after_request(add_security_headers)
    
    # Configure CORS
    configure_cors(app)
    
    # Log security initialization
    app.logger.info("Security features initialized")
