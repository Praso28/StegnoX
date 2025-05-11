"""
StegnoX Backend Application

This module initializes the Flask application and registers all blueprints.
"""

from flask import Flask, jsonify
import os
import logging

from .config.config import config
from .api.v1.auth import auth_bp
from .api.v1.jobs import jobs_bp
from .api.v1.analysis import analysis_bp
from .api.v1.admin import admin_bp
from .utils.security import init_security
from .utils.cache import cache
from .utils.file_scanner import file_scanner
from .utils.performance import performance_monitor
from .utils.error_handler import setup_error_handlers

def create_app(config_name='default'):
    """
    Create and configure the Flask application

    Args:
        config_name (str): Configuration name ('development', 'testing', 'production')

    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)

    # Load configuration
    app_config = config[config_name]
    app_config.init_app(app)

    # Set up error handlers
    setup_error_handlers(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(jobs_bp, url_prefix='/api/v1/jobs')
    app.register_blueprint(analysis_bp, url_prefix='/api/v1/analysis')
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')

    # Initialize security features
    init_security(app)

    # Initialize cache
    cache.init_app(app)

    # Initialize file scanner
    file_scanner.init_app(app)

    # Initialize performance monitoring
    performance_monitor.init_app(app)

    # Root route
    @app.route('/')
    def index():
        return jsonify({
            'name': 'StegnoX API',
            'version': 'v1',
            'status': 'running'
        })

    return app

# Create application instance
app = create_app(os.environ.get('FLASK_CONFIG', 'development'))

if __name__ == '__main__':
    app.run(debug=True)
