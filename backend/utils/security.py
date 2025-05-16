"""
Security utilities for the StegnoX backend
"""

import jwt
from functools import wraps
from flask import request, jsonify, current_app
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

def configure_cors(app):
    """Configure CORS for the application."""
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config.get('CORS_ORIGINS', '*'),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Authorization", "Content-Type"]
        }
    })

def init_security(app):
    """Initialize security features."""
    app.config['JWT_SECRET_KEY'] = app.config.get('JWT_SECRET_KEY', 'dev-key-please-change')
    configure_cors(app)

def generate_token(username, role):
    """Generate a JWT token."""
    return jwt.encode(
        {'username': username, 'role': role},
        current_app.config['JWT_SECRET_KEY'],
        algorithm='HS256'
    )

def token_required(f):
    """Decorator to require JWT token."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Get token from header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({
                'success': False,
                'message': 'Token is missing'
            }), 401

        try:
            # Decode token
            data = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256']
            )
            current_user = {
                'username': data['username'],
                'role': data['role']
            }
        except:
            return jsonify({
                'success': False,
                'message': 'Token is invalid'
            }), 401

        return f(current_user, *args, **kwargs)

    return decorated

def admin_required(f):
    """Decorator to require admin role."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Token is missing!'}), 401

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=["HS256"]
            )
            if data['role'] != 'admin':
                return jsonify({'message': 'Admin privileges required!'}), 403
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated

def hash_password(password):
    """Hash a password."""
    return generate_password_hash(password)

def verify_password(password_hash, password):
    """Verify a password against its hash."""
    return check_password_hash(password_hash, password)

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
