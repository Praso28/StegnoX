"""
Authentication API endpoints
"""

from flask import Blueprint, request, current_app
import os

from ...models.user import User
from ...models.user_db import UserDatabase
from ...auth.auth import generate_token, token_required, admin_required
from ...utils.response import success_response, error_response
from ...utils.rate_limit import rate_limit

# Create blueprint
auth_bp = Blueprint('auth', __name__)

# Initialize user database
user_db = None

@auth_bp.before_request
def before_request():
    """Initialize user database before each request"""
    global user_db
    if user_db is None:
        db_file = os.path.join(current_app.config['STORAGE_DIR'], 'users.json')
        user_db = UserDatabase(db_file)

@auth_bp.route('/register', methods=['POST'])
@rate_limit
def register():
    """Register a new user"""
    data = request.get_json()

    # Validate input
    if not data:
        return error_response('No input data provided', 400)

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return error_response('Missing required fields', 400)

    # Create user
    user = User(username=username, email=email)
    user.set_password(password)

    # Add user to database
    success, message = user_db.add_user(user)

    if not success:
        return error_response(message, 400)

    # Generate token
    token = generate_token(user.user_id, user.role)

    # Return user data and token
    return success_response({
        'user': user.to_dict(),
        'token': token
    }, 'User registered successfully', 201)

@auth_bp.route('/login', methods=['POST'])
@rate_limit
def login():
    """Login a user"""
    data = request.get_json()

    # Validate input
    if not data:
        return error_response('No input data provided', 400)

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return error_response('Missing required fields', 400)

    # Get user
    user = user_db.get_user_by_username(username)

    if not user:
        return error_response('Invalid username or password', 401)

    # Check password
    if not user.check_password(password):
        return error_response('Invalid username or password', 401)

    # Update last login
    user.update_last_login()
    user_db.update_user(user)

    # Generate token
    token = generate_token(user.user_id, user.role)

    # Return user data and token
    return success_response({
        'user': user.to_dict(),
        'token': token
    }, 'Login successful')

@auth_bp.route('/users', methods=['GET'])
@admin_required
@rate_limit
def list_users(user_id, role):
    """List all users (admin only)"""
    users = user_db.list_users()
    return success_response(users, 'Users retrieved successfully')
