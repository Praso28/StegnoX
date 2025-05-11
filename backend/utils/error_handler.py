"""
Error handling utilities for StegnoX backend
"""

import logging
import traceback
import sys
from functools import wraps
from flask import jsonify, current_app

logger = logging.getLogger(__name__)

class AppError(Exception):
    """Base exception class for application errors"""
    def __init__(self, message, status_code=500, payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Convert exception to dictionary for JSON response"""
        result = {}
        result['success'] = False
        result['message'] = self.message
        if self.payload:
            result['errors'] = self.payload
        return result

def handle_error(func):
    """Decorator to handle errors in API endpoints"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AppError as e:
            logger.error(f"Application error: {str(e)}")
            return jsonify(e.to_dict()), e.status_code
        except Exception as e:
            # Log the full traceback for unexpected errors
            logger.error(f"Unexpected error: {str(e)}")
            logger.error(traceback.format_exc())
            
            # In development mode, include the traceback in the response
            if current_app.config.get('DEBUG', False):
                error_details = {
                    'exception': str(e),
                    'traceback': traceback.format_exc()
                }
                return jsonify({
                    'success': False,
                    'message': 'Internal server error',
                    'errors': error_details
                }), 500
            else:
                # In production, don't expose internal details
                return jsonify({
                    'success': False,
                    'message': 'Internal server error'
                }), 500
    
    return wrapper

def setup_error_handlers(app):
    """Set up global error handlers for the Flask app"""
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Resource not found',
            'error': str(error)
        }), 404
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'message': 'Bad request',
            'error': str(error)
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'message': 'Unauthorized',
            'error': str(error)
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'success': False,
            'message': 'Forbidden',
            'error': str(error)
        }), 403
    
    @app.errorhandler(500)
    def server_error(error):
        logger.error(f"Server error: {str(error)}")
        logger.error(traceback.format_exc())
        
        if app.config.get('DEBUG', False):
            error_details = {
                'exception': str(error),
                'traceback': traceback.format_exc()
            }
            return jsonify({
                'success': False,
                'message': 'Internal server error',
                'errors': error_details
            }), 500
        else:
            return jsonify({
                'success': False,
                'message': 'Internal server error'
            }), 500
