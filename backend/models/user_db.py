"""
User database for storing and retrieving users
"""

import os
import json
import threading
from .user import User

class UserDatabase:
    """Simple JSON-based user database"""
    
    def __init__(self, db_file):
        """
        Initialize the user database
        
        Args:
            db_file (str): Path to the database file
        """
        self.db_file = db_file
        self.users = {}
        self.lock = threading.RLock()
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(db_file), exist_ok=True)
        
        # Load existing users
        self._load_users()
    
    def _load_users(self):
        """Load users from the database file"""
        if not os.path.exists(self.db_file):
            return
        
        try:
            with open(self.db_file, 'r') as f:
                user_data = json.load(f)
                
                for user_id, data in user_data.items():
                    self.users[user_id] = User.from_dict(data)
        except Exception as e:
            print(f"Error loading users: {str(e)}")
    
    def _save_users(self):
        """Save users to the database file"""
        try:
            user_data = {}
            for user_id, user in self.users.items():
                user_dict = user.to_dict()
                user_dict['password_hash'] = user.password_hash
                user_data[user_id] = user_dict
            
            with open(self.db_file, 'w') as f:
                json.dump(user_data, f, indent=2)
        except Exception as e:
            print(f"Error saving users: {str(e)}")
    
    def add_user(self, user):
        """
        Add a user to the database
        
        Args:
            user (User): User to add
            
        Returns:
            bool: True if successful, False otherwise
        """
        with self.lock:
            # Check if username or email already exists
            for existing_user in self.users.values():
                if existing_user.username == user.username:
                    return False, "Username already exists"
                if existing_user.email == user.email:
                    return False, "Email already exists"
            
            # Add user
            self.users[user.user_id] = user
            self._save_users()
            
            return True, "User added successfully"
    
    def get_user_by_id(self, user_id):
        """
        Get a user by ID
        
        Args:
            user_id (str): User ID
            
        Returns:
            User: User object or None if not found
        """
        with self.lock:
            return self.users.get(user_id)
    
    def get_user_by_username(self, username):
        """
        Get a user by username
        
        Args:
            username (str): Username
            
        Returns:
            User: User object or None if not found
        """
        with self.lock:
            for user in self.users.values():
                if user.username == username:
                    return user
            return None
    
    def get_user_by_email(self, email):
        """
        Get a user by email
        
        Args:
            email (str): Email address
            
        Returns:
            User: User object or None if not found
        """
        with self.lock:
            for user in self.users.values():
                if user.email == email:
                    return user
            return None
    
    def update_user(self, user):
        """
        Update a user in the database
        
        Args:
            user (User): User to update
            
        Returns:
            bool: True if successful, False otherwise
        """
        with self.lock:
            if user.user_id not in self.users:
                return False
            
            self.users[user.user_id] = user
            self._save_users()
            
            return True
    
    def delete_user(self, user_id):
        """
        Delete a user from the database
        
        Args:
            user_id (str): User ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        with self.lock:
            if user_id not in self.users:
                return False
            
            del self.users[user_id]
            self._save_users()
            
            return True
    
    def list_users(self):
        """
        List all users
        
        Returns:
            list: List of user dictionaries
        """
        with self.lock:
            return [user.to_dict() for user in self.users.values()]
