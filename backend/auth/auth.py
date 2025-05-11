"""
Authentication module for StegnoX backend
"""

import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app

def generate_token(user_id, role='user', expiration=None):
    """
    Generate a JWT token
    
    Args:
        user_id (str): User ID
        role (str): User role
        expiration (datetime, optional): Token expiration time
        
    Returns:
        str: JWT token
    """
    if expiration is None:
        expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    
    payload = {
        'exp': expiration,
        'iat': datetime.datetime.utcnow(),
        'sub': user_id,
        'role': role
    }
    
    return jwt.encode(
        payload,
        current_app.config.get('JWT_SECRET_KEY'),
        algorithm='HS256'
    )

def decode_token(token):
    """
    Decode a JWT token
    
    Args:
        token (str): JWT token
        
    Returns:
        dict: Token payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            current_app.config.get('JWT_SECRET_KEY'),
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """
    Decorator for routes that require a valid token
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        # Decode token
        payload = decode_token(token)
        if not payload:
            return jsonify({'message': 'Token is invalid or expired'}), 401
        
        # Add user_id to kwargs
        kwargs['user_id'] = payload['sub']
        kwargs['role'] = payload.get('role', 'user')
        
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    """
    Decorator for routes that require admin privileges
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        # Decode token
        payload = decode_token(token)
        if not payload:
            return jsonify({'message': 'Token is invalid or expired'}), 401
        
        # Check if user is admin
        if payload.get('role') != 'admin':
            return jsonify({'message': 'Admin privileges required'}), 403
        
        # Add user_id to kwargs
        kwargs['user_id'] = payload['sub']
        kwargs['role'] = payload.get('role', 'user')
        
        return f(*args, **kwargs)
    
    return decorated
