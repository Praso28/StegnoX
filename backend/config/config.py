"""
Configuration settings for the StegnoX backend
"""

import os
import secrets
from datetime import timedelta

class Config:
    """Base configuration"""
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    DEBUG = False
    TESTING = False

    # File upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB limit
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

    # JWT settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or secrets.token_hex(32)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Database settings
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///stegnox.db'

    # Storage settings
    STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'storage')

    # Queue settings
    QUEUE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'queue')

    # Rate limiting settings
    RATE_LIMIT = 100  # Maximum number of requests per window
    RATE_LIMIT_WINDOW = 3600  # Window size in seconds (1 hour)
    RATE_LIMIT_BY_IP = True  # Limit by IP address
    RATE_LIMIT_BY_USER = True  # Limit by user ID

    # CORS settings
    CORS_ORIGINS = '*'  # Allow all origins in development

    # Caching settings
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    CACHE_DISABLED_IN_DEBUG = True
    CACHE_MIN_DURATION = 0.1  # Only cache functions that take longer than 100ms

    # Performance monitoring settings
    PERFORMANCE_MONITORING_ENABLED = True
    LOG_SLOW_REQUESTS = True
    SLOW_REQUEST_THRESHOLD = 1.0  # seconds

    # Ensure directories exist
    @classmethod
    def init_app(cls, app):
        """Initialize application with this configuration"""
        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(cls.STORAGE_DIR, exist_ok=True)
        os.makedirs(cls.QUEUE_DIR, exist_ok=True)

        # Set Flask config
        app.config.from_object(cls)

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    # Override with production settings

    # Stricter rate limiting for production
    RATE_LIMIT = 60  # 60 requests per hour
    RATE_LIMIT_WINDOW = 3600  # 1 hour window

    # Restrictive CORS for production
    CORS_ORIGINS = ['https://stegnox.example.com', 'https://www.stegnox.example.com']

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
