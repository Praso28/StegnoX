"""
User model for authentication and authorization
"""

import uuid
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    """User model for authentication"""
    
    def __init__(self, username, email, password=None, user_id=None, role='user'):
        """
        Initialize a new user
        
        Args:
            username (str): Username
            email (str): Email address
            password (str, optional): Password (will be hashed)
            user_id (str, optional): User ID (will be generated if None)
            role (str): User role ('user' or 'admin')
        """
        self.user_id = user_id or str(uuid.uuid4())
        self.username = username
        self.email = email
        self.role = role
        self.created_at = datetime.datetime.now().isoformat()
        self.last_login = None
        
        if password:
            self.set_password(password)
        else:
            self.password_hash = None
    
    def set_password(self, password):
        """
        Set the password hash
        
        Args:
            password (str): Plain text password
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Check if the password is correct
        
        Args:
            password (str): Plain text password to check
            
        Returns:
            bool: True if password is correct, False otherwise
        """
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        """Update the last login timestamp"""
        self.last_login = datetime.datetime.now().isoformat()
    
    def to_dict(self):
        """
        Convert user to dictionary
        
        Returns:
            dict: User data
        """
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at,
            'last_login': self.last_login
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a user from dictionary data
        
        Args:
            data (dict): User data
            
        Returns:
            User: User object
        """
        user = cls(
            username=data['username'],
            email=data['email'],
            user_id=data.get('user_id')
        )
        user.password_hash = data.get('password_hash')
        user.role = data.get('role', 'user')
        user.created_at = data.get('created_at', user.created_at)
        user.last_login = data.get('last_login')
        
        return user
