#!/usr/bin/env python3
"""
StegnoX Project Cleanup Script

This script cleans up the StegnoX project directory by:
1. Removing duplicate files in the root directory
2. Organizing configuration files into appropriate directories
3. Creating a deployment directory for deployment-related files
"""

import os
import shutil
import sys

def print_status(message):
    """Print a status message with formatting"""
    print(f"\n[*] {message}")

def print_success(message):
    """Print a success message with formatting"""
    print(f"[+] {message}")

def print_error(message):
    """Print an error message with formatting"""
    print(f"[!] {message}")

def create_directory(directory):
    """Create a directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print_success(f"Created directory: {directory}")
    else:
        print_status(f"Directory already exists: {directory}")

def remove_file(file_path):
    """Remove a file if it exists"""
    if os.path.exists(file_path):
        os.remove(file_path)
        print_success(f"Removed file: {file_path}")
    else:
        print_status(f"File does not exist: {file_path}")

def move_file(source, destination):
    """Move a file from source to destination"""
    if os.path.exists(source):
        # Create destination directory if it doesn't exist
        dest_dir = os.path.dirname(destination)
        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        # Move the file
        shutil.move(source, destination)
        print_success(f"Moved file: {source} -> {destination}")
    else:
        print_error(f"Source file does not exist: {source}")

def main():
    """Main function to clean up the project"""
    print_status("Starting StegnoX project cleanup")
    
    # 1. Remove duplicate files in the root directory
    print_status("Removing duplicate files in root directory")
    
    # Remove stegnox_engine.py from root (duplicate of engine/stegnox_engine.py)
    remove_file("stegnox_engine.py")
    
    # Remove app.py from root (older version of backend/app.py)
    remove_file("app.py")
    
    # Remove architecture.md from root (older version of docs/architecture.md)
    remove_file("architecture.md")
    
    # 2. Create deployment directory and move deployment files there
    print_status("Organizing deployment files")
    create_directory("deployment")
    
    # Move deployment files to deployment directory
    move_file("deploy.sh", "deployment/deploy.sh")
    move_file("docker-compose.yml", "deployment/docker-compose.yml")
    move_file("docker-compose.dev.yml", "deployment/docker-compose.dev.yml")
    move_file("docker-compose.prod.yml", "deployment/docker-compose.prod.yml")
    
    # 3. Move build_desktop.py to desktop directory
    print_status("Moving build script to desktop directory")
    move_file("build_desktop.py", "desktop/build_desktop.py")
    
    # 4. Update README.md to reflect the new structure
    print_status("Updating README.md with new directory structure")
    
    # This would be better done with a more sophisticated approach,
    # but for simplicity we'll just print a message
    print_success("Please update README.md manually to reflect the new directory structure")
    
    print_status("Cleanup complete!")
    print_status("New directory structure:")
    print("""
    StegnoX/
    ├── backend/           # Flask API backend
    ├── deployment/        # Deployment configuration files
    │   ├── deploy.sh
    │   ├── docker-compose.yml
    │   ├── docker-compose.dev.yml
    │   └── docker-compose.prod.yml
    ├── desktop/           # Desktop GUI application
    │   ├── build_desktop.py  # Desktop build script
    │   └── ...
    ├── docs/              # Documentation
    ├── engine/            # Steganography engine
    ├── examples/          # Example scripts
    ├── frontend/          # React web frontend
    ├── queue/             # Job queue system
    ├── storage/           # Storage service
    ├── tests/             # Test files
    ├── main.py            # Main entry point
    ├── README.md          # Project documentation
    └── requirements.txt   # Python dependencies
    """)

if __name__ == "__main__":
    main()
