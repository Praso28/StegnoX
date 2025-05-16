"""
Flask application factory
"""

import os
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .api.v1.auth import auth_bp
from .api.v1.analysis import analysis_bp
from .api.v1.jobs import jobs_bp
from .utils.security import init_security
from .utils.db import init_db, db

def create_app(config_name=None):
    """Create Flask application."""
    app = Flask(__name__)
    
    # Load the default configuration
    app.config.from_object('config.default')

    # Load the configuration from the instance folder
    app.config.from_pyfile('config.py', silent=True)

    # Load the file specified by the APP_CONFIG_FILE environment variable
    # Variables defined here will override those in the default configuration
    if config_name:
        app.config.from_object(f'config.{config_name}')

    # Initialize Flask extensions
    init_db(app)
    init_security(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(analysis_bp, url_prefix='/api/v1/analysis')
    app.register_blueprint(jobs_bp, url_prefix='/api/v1/jobs')

    # Frontend routes
    @app.route('/')
    def index():
        """Render the homepage."""
        return render_template('home.html')

    @app.route('/analyze')
    def analyze():
        """Render the analyze page."""
        return render_template('analyze.html')

    @app.route('/encode')
    def encode():
        """Render the encode page."""
        return render_template('encode.html')

    @app.route('/jobs')
    def jobs():
        """Render the jobs page."""
        return render_template('jobs.html')

    # API root
    @app.route('/api/v1')
    def api_index():
        """Return basic API information."""
        return jsonify({
            'name': 'StegnoX API',
            'version': 'v1',
            'status': 'running'
        })

    return app

# Only create the application instance when running the app directly
if __name__ == '__main__':
    app = create_app(os.environ.get('FLASK_CONFIG', 'development'))
    app.run()
