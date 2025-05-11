"""
File utility functions for StegnoX backend
"""

import os
import uuid
import logging
from werkzeug.utils import secure_filename
from flask import current_app
from .file_scanner import file_scanner

def allowed_file(filename):
    """
    Check if a file has an allowed extension

    Args:
        filename (str): Filename to check

    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file, custom_filename=None):
    """
    Save an uploaded file

    Args:
        file: File object from request.files
        custom_filename (str, optional): Custom filename to use

    Returns:
        str: Path to the saved file or None if file is invalid
    """
    logger = logging.getLogger('stegnox.file_utils')

    if file and allowed_file(file.filename):
        try:
            if custom_filename:
                filename = secure_filename(custom_filename)
            else:
                # Generate a unique filename
                original_ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"{uuid.uuid4()}.{original_ext}"

            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Scan the file for security issues
            is_safe, message = file_scanner.scan_file(filepath)

            if not is_safe:
                logger.warning(f"File security scan failed: {message}")
                # Remove the unsafe file
                if os.path.exists(filepath):
                    os.remove(filepath)
                return None

            logger.info(f"File saved and passed security scan: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Error saving uploaded file: {str(e)}")
            # Clean up if there was an error
            if 'filepath' in locals() and os.path.exists(filepath):
                os.remove(filepath)

    return None

def get_file_extension(filename):
    """
    Get the extension of a file

    Args:
        filename (str): Filename

    Returns:
        str: File extension or empty string if no extension
    """
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return ""
