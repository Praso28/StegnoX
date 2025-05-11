"""
File scanning utilities for StegnoX backend
"""

import os
import hashlib
import logging
import magic
import re
import imghdr
from PIL import Image
from flask import current_app

class FileScanner:
    """File scanner for security checks"""

    def __init__(self, app=None):
        """
        Initialize the file scanner

        Args:
            app (Flask, optional): Flask application
        """
        self.app = app
        self.logger = logging.getLogger('stegnox.file_scanner')

        # Initialize default settings
        self.max_file_size = 16 * 1024 * 1024  # 16MB
        self.allowed_mime_types = [
            'image/jpeg',
            'image/png',
            'image/gif',
            'image/bmp'
        ]
        self.allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initialize the scanner with a Flask application

        Args:
            app (Flask): Flask application
        """
        self.app = app

        # Get configuration from app
        self.max_file_size = app.config.get('MAX_CONTENT_LENGTH', self.max_file_size)
        self.allowed_extensions = [f".{ext}" for ext in app.config.get('ALLOWED_EXTENSIONS', [])]

        self.logger.info(f"File scanner initialized with max size: {self.max_file_size} bytes")

    def scan_file(self, file_path):
        """
        Scan a file for security issues

        Args:
            file_path (str): Path to the file

        Returns:
            tuple: (is_safe, message)
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return False, "File does not exist"

            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > self.max_file_size:
                return False, f"File size exceeds maximum allowed size ({file_size} > {self.max_file_size})"

            # Check file extension
            _, ext = os.path.splitext(file_path)
            if ext.lower() not in self.allowed_extensions:
                return False, f"File extension {ext} not allowed"

            # Check MIME type
            mime_type = self._get_mime_type(file_path)
            if mime_type not in self.allowed_mime_types:
                return False, f"File type {mime_type} not allowed"

            # Verify image integrity
            if not self._verify_image(file_path):
                return False, "Invalid image file"

            # Calculate file hash
            file_hash = self._calculate_hash(file_path)

            # Log scan result
            self.logger.info(f"File scan passed: {file_path} (size: {file_size}, type: {mime_type}, hash: {file_hash})")

            return True, "File passed security scan"

        except Exception as e:
            self.logger.error(f"Error scanning file {file_path}: {str(e)}")
            return False, f"Error scanning file: {str(e)}"

    def _get_mime_type(self, file_path):
        """
        Get the MIME type of a file

        Args:
            file_path (str): Path to the file

        Returns:
            str: MIME type
        """
        try:
            # Try using python-magic if available
            return magic.from_file(file_path, mime=True)
        except (ImportError, AttributeError):
            # Fallback to imghdr for image type detection
            img_type = imghdr.what(file_path)
            if img_type:
                return f"image/{img_type}"

            # Last resort: use file extension
            _, ext = os.path.splitext(file_path)
            ext = ext.lower().lstrip('.')

            mime_map = {
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'png': 'image/png',
                'gif': 'image/gif',
                'bmp': 'image/bmp'
            }

            return mime_map.get(ext, 'application/octet-stream')

    def _verify_image(self, file_path):
        """
        Verify that a file is a valid image

        Args:
            file_path (str): Path to the file

        Returns:
            bool: True if valid image, False otherwise
        """
        try:
            # Try to open the image with PIL
            with Image.open(file_path) as img:
                # Verify image by loading it
                img.verify()

            # Additional check: try to get image size
            with Image.open(file_path) as img:
                img.size

            return True
        except Exception as e:
            self.logger.warning(f"Image verification failed for {file_path}: {str(e)}")
            return False

    def _calculate_hash(self, file_path):
        """
        Calculate SHA-256 hash of a file

        Args:
            file_path (str): Path to the file

        Returns:
            str: File hash
        """
        sha256 = hashlib.sha256()

        with open(file_path, 'rb') as f:
            # Read in chunks to handle large files
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)

        return sha256.hexdigest()

# Create a global scanner instance
file_scanner = FileScanner()
