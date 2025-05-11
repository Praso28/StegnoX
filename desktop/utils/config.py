"""
Configuration management for the StegnoX desktop application
"""

import os
import json
import tkinter as tk
from tkinter import messagebox

class Config:
    """Configuration manager for the StegnoX desktop application"""

    DEFAULT_CONFIG = {
        "theme": "light",
        "max_image_size": (800, 800),
        "default_output_dir": "",
        "recent_files": [],
        "max_recent_files": 10,
        "default_encoding_method": "lsb",
        "show_advanced_options": False,
        "auto_save_results": True,
        "results_dir": "",
        "batch_processing": {
            "max_threads": 4,
            "auto_save": True
        }
    }

    def __init__(self):
        """Initialize the configuration manager"""
        self.config_dir = os.path.join(os.path.expanduser("~"), ".stegnox")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.config = self.DEFAULT_CONFIG.copy()
        self.load_config()

    def load_config(self):
        """Load configuration from file"""
        try:
            if not os.path.exists(self.config_dir):
                os.makedirs(self.config_dir)

            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Update config with loaded values, keeping defaults for missing keys
                    self._update_dict_recursive(self.config, loaded_config)
        except Exception as e:
            messagebox.showwarning(
                "Configuration Error",
                f"Failed to load configuration: {str(e)}\nUsing default settings."
            )

    def save_config(self):
        """Save configuration to file"""
        try:
            if not os.path.exists(self.config_dir):
                os.makedirs(self.config_dir)

            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            messagebox.showwarning(
                "Configuration Error",
                f"Failed to save configuration: {str(e)}"
            )

    def get(self, key, default=None):
        """Get a configuration value"""
        keys = key.split('.')
        value = self.config

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key, value):
        """Set a configuration value"""
        keys = key.split('.')
        config = self.config

        # Navigate to the nested dictionary
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]

        # Set the value
        config[keys[-1]] = value
        self.save_config()

    def add_recent_file(self, file_path):
        """Add a file to the recent files list"""
        recent_files = self.get('recent_files', [])

        # Remove if already exists
        if file_path in recent_files:
            recent_files.remove(file_path)

        # Add to the beginning
        recent_files.insert(0, file_path)

        # Limit the number of recent files
        max_recent = self.get('max_recent_files', 10)
        if len(recent_files) > max_recent:
            recent_files = recent_files[:max_recent]

        self.set('recent_files', recent_files)

    def _update_dict_recursive(self, target, source):
        """Update a dictionary recursively"""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._update_dict_recursive(target[key], value)
            else:
                target[key] = value

    def reset_to_defaults(self):
        """Reset configuration to default values"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save_config()
