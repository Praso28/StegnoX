"""
Unit tests for the StegnoX desktop application
"""

import unittest
import os
import sys
import tkinter as tk
from unittest.mock import MagicMock, patch

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from desktop.app import StegnoXApp

class TestDesktopApp(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        # Create a mock root window
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window
        
        # Create a directory for logs if it doesn't exist
        os.makedirs(os.path.join(os.path.expanduser("~"), ".stegnox"), exist_ok=True)
        
        # Patch the engine to avoid actual file operations
        self.engine_patcher = patch('engine.stegnox_engine.StegnoxEngine')
        self.mock_engine = self.engine_patcher.start()
        
        # Initialize the app with the mock engine
        self.app = StegnoXApp(self.root)
        
    def tearDown(self):
        """Clean up test environment"""
        self.engine_patcher.stop()
        self.root.destroy()
    
    def test_initialization(self):
        """Test that the app initializes correctly"""
        self.assertIsNotNone(self.app)
        self.assertEqual(self.app.root, self.root)
        self.assertIsNotNone(self.app.engine)
    
    def test_show_help(self):
        """Test the show_help method"""
        # Mock the messagebox.showinfo method
        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.show_help()
            mock_showinfo.assert_called_once()
    
    def test_set_status(self):
        """Test the set_status method"""
        test_message = "Test status message"
        # Mock the status_bar
        self.app.status_bar = MagicMock()
        self.app.set_status(test_message)
        self.app.status_bar.set_status.assert_called_once_with(test_message)

if __name__ == '__main__':
    unittest.main()
