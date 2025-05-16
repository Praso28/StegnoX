"""
Database utilities for the StegnoX backend
"""

from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object
db = SQLAlchemy()

def init_db(app):
    """Initialize the database."""
    db.init_app(app) 