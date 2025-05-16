"""
Default configuration
"""

import os

# Flask
DEBUG = False
TESTING = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-please-change')

# Database
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///stegnox.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-key-please-change')

# CORS
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')

# File Upload
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'} 