"""
StegnoX Backend Package
"""

from flask import Flask

def create_app(config_name='default'):
    app = Flask(__name__, instance_relative_config=True)
    
    # Basic configuration
    app.config.update(
        TESTING=(config_name == 'testing'),
        SECRET_KEY='dev',
        JWT_SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///test.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    
    # Register routes
    @app.route('/')
    def index():
        return {'name': 'StegnoX API', 'version': 'v1', 'status': 'running'}
    
    return app