"""
Pytest configuration file
"""

import os
import sys
import pytest
import tempfile
import shutil
from PIL import Image
from backend.app import create_app
from backend.utils.db import db as _db

# Add parent directory to path to allow imports
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

def pytest_configure(config):
    """Configure pytest"""
    # Create necessary directories
    dirs = ['tests/data', 'storage/temp', 'backend/instance']
    for d in dirs:
        os.makedirs(d, exist_ok=True)

@pytest.fixture(scope="session")
def test_db():
    """Create a test database"""
    db_path = os.path.join('backend', 'instance', 'test.db')
    if os.path.exists(db_path):
        os.remove(db_path)
    
    import sqlite3
    conn = sqlite3.connect(db_path)
    conn.close()
    return db_path

@pytest.fixture(scope="session")
def temp_dir():
    """Create a temporary directory for test files"""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    # Cleanup
    try:
        shutil.rmtree(temp_path)
    except:
        pass

@pytest.fixture(scope="session")
def test_image(temp_dir):
    """Create a test image"""
    image_path = os.path.join(temp_dir, 'test_image.png')
    img = Image.new('RGB', (100, 100), color='white')
    img.save(image_path)
    return image_path

@pytest.fixture(scope="session", autouse=True)
def setup_test_data(temp_dir):
    """Create test data directory and sample images"""
    # Create test data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)

    # Create a sample test image
    test_image_path = os.path.join(data_dir, 'test_image.png')
    if not os.path.exists(test_image_path):
        img = Image.new('RGB', (100, 100), color='white')
        img.save(test_image_path)

    # Create test images with different formats
    formats = [('png', 'RGB'), ('jpeg', 'RGB'), ('bmp', 'RGB')]
    for fmt, mode in formats:
        img_path = os.path.join(data_dir, f'test_image.{fmt}')
        if not os.path.exists(img_path):
            img = Image.new(mode, (100, 100), color='white')
            img.save(img_path)

    return data_dir

@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment variables"""
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['JWT_SECRET_KEY'] = 'test_secret_key'
    os.environ['DATABASE_URL'] = 'sqlite:///test.db'
    
    # Ensure the backend package is importable
    backend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend')
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)

@pytest.fixture(scope='session')
def app():
    """Create application for the tests."""
    os.environ['FLASK_CONFIG'] = 'testing'
    _app = create_app('testing')
    
    # Set testing configuration
    _app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'CORS_ORIGINS': '*',
        'JWT_SECRET_KEY': 'test-key',
        'SECRET_KEY': 'test-key'
    })
    
    # Create application context
    ctx = _app.app_context()
    ctx.push()

    # Create all database tables
    _db.create_all()

    yield _app

    # Clean up
    _db.session.remove()
    _db.drop_all()
    ctx.pop()

@pytest.fixture(scope='function')
def client(app):
    """Create a test client."""
    return app.test_client()

@pytest.fixture(scope='function')
def db(app):
    """Create a clean database for tests."""
    _db.app = app
    
    # Clear any existing data
    for table in reversed(_db.metadata.sorted_tables):
        _db.session.execute(table.delete())
    _db.session.commit()

    yield _db

    # Clean up after test
    _db.session.rollback()
    for table in reversed(_db.metadata.sorted_tables):
        _db.session.execute(table.delete())
    _db.session.commit()

@pytest.fixture(scope='function')
def session(db):
    """Create a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()
    
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    
    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove() 