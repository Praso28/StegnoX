"""
Testing configuration
"""

import os

# Flask
DEBUG = False
TESTING = True
SECRET_KEY = 'test-key'
SERVER_NAME = 'localhost:5000'

# Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT
JWT_SECRET_KEY = 'test-key'

# CORS
CORS_ORIGINS = '*'

# Storage
STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', 'storage')
UPLOAD_FOLDER = os.path.join(STORAGE_DIR, 'uploads')
RESULTS_FOLDER = os.path.join(STORAGE_DIR, 'results')
QUEUE_DIR = os.path.join(STORAGE_DIR, 'queue')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Create storage directories if they don't exist
os.makedirs(STORAGE_DIR, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(QUEUE_DIR, exist_ok=True)

# Test user
TEST_USER = {
    'username': 'test_user',
    'password': 'test_password',
    'role': 'user'
} 