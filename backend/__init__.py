"""
StegnoX Backend Package
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='default'):
    app = Flask(__name__, instance_relative_config=True)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Basic configuration
    app.config.update(
        TESTING=(config_name == 'testing'),
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///test.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register routes
    @app.route('/')
    def index():
        return {'name': 'StegnoX API', 'version': 'v1', 'status': 'running'}
    
    return app