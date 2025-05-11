"""
Response utility functions for StegnoX backend
"""

from flask import jsonify

def success_response(data=None, message=None, status_code=200):
    """
    Create a success response
    
    Args:
        data: Response data
        message (str, optional): Success message
        status_code (int): HTTP status code
        
    Returns:
        tuple: (response, status_code)
    """
    response = {
        'success': True
    }
    
    if data is not None:
        response['data'] = data
    
    if message:
        response['message'] = message
    
    return jsonify(response), status_code

def error_response(message, status_code=400, errors=None):
    """
    Create an error response
    
    Args:
        message (str): Error message
        status_code (int): HTTP status code
        errors (dict, optional): Detailed error information
        
    Returns:
        tuple: (response, status_code)
    """
    response = {
        'success': False,
        'message': message
    }
    
    if errors:
        response['errors'] = errors
    
    return jsonify(response), status_code
