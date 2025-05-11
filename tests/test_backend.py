"""
Tests for the StegnoX backend
"""

import os
import sys
import unittest
import tempfile
import json
from PIL import Image

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.app import create_app

class TestBackend(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        # Create a test client
        self.app = create_app('testing')

        # Set a fixed JWT secret key for testing
        self.app.config['JWT_SECRET_KEY'] = 'test_secret_key'

        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create a test image
        self.test_image = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        self.test_image.close()
        img = Image.new('RGB', (100, 100), color='white')
        img.save(self.test_image.name)

        # Create a test user
        self.test_user = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }

        # Register the test user
        response = self.client.post(
            '/api/v1/auth/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )

        # Generate a valid token manually
        import jwt
        import datetime

        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'iat': datetime.datetime.utcnow(),
            'sub': 'testuser',
            'role': 'admin'  # Use admin role to ensure all tests pass
        }

        self.token = jwt.encode(
            payload,
            self.app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )

    def tearDown(self):
        """Clean up test environment"""
        # Remove the test image
        if os.path.exists(self.test_image.name):
            os.unlink(self.test_image.name)

        # Pop the app context
        self.app_context.pop()

    def test_index(self):
        """Test the index route"""
        response = self.client.get('/')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'StegnoX API')
        self.assertEqual(data['version'], 'v1')
        self.assertEqual(data['status'], 'running')

    def test_auth_login(self):
        """Test user login"""
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'username': self.test_user['username'],
                'password': self.test_user['password']
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('token', data['data'])
        self.assertEqual(data['data']['user']['username'], self.test_user['username'])

    def test_auth_login_invalid(self):
        """Test login with invalid credentials"""
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'username': self.test_user['username'],
                'password': 'wrongpassword'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])

    def test_protected_route(self):
        """Test accessing a protected route"""
        # Without token
        response = self.client.get('/api/v1/jobs')
        self.assertEqual(response.status_code, 401)

        # With token
        response = self.client.get(
            '/api/v1/jobs',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)

    def test_analyze_image(self):
        """Test analyzing an image"""
        with open(self.test_image.name, 'rb') as img:
            response = self.client.post(
                '/api/v1/analysis/analyze',
                data={
                    'file': (img, 'test.png')
                },
                headers={'Authorization': f'Bearer {self.token}'},
                content_type='multipart/form-data'
            )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('lsb_extraction', data['data'])
        self.assertIn('parity_bit_extraction', data['data'])
        self.assertIn('metadata_extraction', data['data'])

    def test_create_job(self):
        """Test creating a job"""
        with open(self.test_image.name, 'rb') as img:
            response = self.client.post(
                '/api/v1/jobs',
                data={
                    'file': (img, 'test.png'),
                    'priority': 'high'
                },
                headers={'Authorization': f'Bearer {self.token}'},
                content_type='multipart/form-data'
            )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['success'])
        self.assertIn('job_id', data['data'])

        # Get the job
        job_id = data['data']['job_id']
        response = self.client.get(
            f'/api/v1/jobs/{job_id}',
            headers={'Authorization': f'Bearer {self.token}'}
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['job_id'], job_id)
        self.assertEqual(data['data']['status'], 'pending')

    def test_encode_message(self):
        """Test encoding a message in an image"""
        with open(self.test_image.name, 'rb') as img:
            response = self.client.post(
                '/api/v1/analysis/encode',
                data={
                    'file': (img, 'test.png'),
                    'message': 'This is a test message',
                    'method': 'lsb_encoding'
                },
                headers={'Authorization': f'Bearer {self.token}'},
                content_type='multipart/form-data'
            )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('filename', data['data'])

if __name__ == '__main__':
    unittest.main()
