"""
Tests for the StegnoX backend
"""

import os
import sys
import tempfile
import json
import jwt
import datetime
import pytest
from PIL import Image

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_image():
    """Create a test image file"""
    test_image = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    test_image.close()
    img = Image.new('RGB', (100, 100), color='white')
    img.save(test_image.name)
    
    yield test_image.name
    
    if os.path.exists(test_image.name):
        os.unlink(test_image.name)

@pytest.fixture
def test_user():
    """Create a test user data"""
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    }

@pytest.fixture
def auth_token(app, client, test_user):
    """Create and register a test user, return auth token"""
    # Register the test user
    client.post(
        '/api/v1/auth/register',
        data=json.dumps(test_user),
        content_type='application/json'
    )

    # Generate a valid token
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow(),
        'sub': test_user['username'],
        'role': 'admin'
    }

    return jwt.encode(
        payload,
        app.config['JWT_SECRET_KEY'],
        algorithm='HS256'
    )

def test_index(client):
    """Test the index route"""
    response = client.get('/')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['name'] == 'StegnoX API'
    assert data['version'] == 'v1'
    assert data['status'] == 'running'

def test_auth_login(client, test_user):
    """Test user login"""
    response = client.post(
        '/api/v1/auth/login',
        data=json.dumps({
            'username': test_user['username'],
            'password': test_user['password']
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['success'] is True
    assert 'token' in data['data']
    assert data['data']['user']['username'] == test_user['username']

def test_auth_login_invalid(client, test_user):
    """Test login with invalid credentials"""
    response = client.post(
        '/api/v1/auth/login',
        data=json.dumps({
            'username': test_user['username'],
            'password': 'wrongpassword'
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['success'] is False

def test_protected_route(client, auth_token):
    """Test accessing a protected route"""
    # Without token
    response = client.get('/api/v1/jobs')
    assert response.status_code == 401

    # With token
    response = client.get(
        '/api/v1/jobs',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 200

def test_analyze_image(client, auth_token, test_image):
    """Test analyzing an image"""
    with open(test_image, 'rb') as img:
        response = client.post(
            '/api/v1/analysis/analyze',
            data={
                'file': (img, 'test.png')
            },
            headers={'Authorization': f'Bearer {auth_token}'},
            content_type='multipart/form-data'
        )

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['success'] is True
    assert 'lsb_extraction' in data['data']
    assert 'parity_bit_extraction' in data['data']
    assert 'metadata_extraction' in data['data']

def test_create_job(client, auth_token, test_image):
    """Test creating a job"""
    with open(test_image, 'rb') as img:
        response = client.post(
            '/api/v1/jobs',
            data={
                'file': (img, 'test.png'),
                'priority': 'high'
            },
            headers={'Authorization': f'Bearer {auth_token}'},
            content_type='multipart/form-data'
        )

    data = json.loads(response.data)

    assert response.status_code == 201
    assert data['success'] is True
    assert 'job_id' in data['data']

    # Get the job
    job_id = data['data']['job_id']
    response = client.get(
        f'/api/v1/jobs/{job_id}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['success'] is True
    assert data['data']['job_id'] == job_id
    assert data['data']['status'] == 'pending'

def test_encode_message(client, auth_token, test_image):
    """Test encoding a message in an image"""
    with open(test_image, 'rb') as img:
        response = client.post(
            '/api/v1/analysis/encode',
            data={
                'file': (img, 'test.png'),
                'message': 'This is a test message',
                'method': 'lsb_encoding'
            },
            headers={'Authorization': f'Bearer {auth_token}'},
            content_type='multipart/form-data'
        )

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['success'] is True
