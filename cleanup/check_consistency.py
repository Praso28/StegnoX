#!/usr/bin/env python3
"""
StegnoX Project Consistency Checker

This script checks for any remaining issues or inconsistencies in the project structure
after the cleanup process.
"""

import os
import sys
import re

def print_status(message):
    """Print a status message with formatting"""
    print(f"\n[*] {message}")

def print_success(message):
    """Print a success message with formatting"""
    print(f"[+] {message}")

def print_warning(message):
    """Print a warning message with formatting"""
    print(f"[!] {message}")

def check_imports():
    """Check for any imports that might be broken after moving files"""
    print_status("Checking for potentially broken imports")
    
    issues_found = False
    
    # Check for imports of moved files
    patterns = [
        (r"from\s+stegnox_engine\s+import", "Root stegnox_engine.py was moved to engine/stegnox_engine.py"),
        (r"import\s+stegnox_engine", "Root stegnox_engine.py was moved to engine/stegnox_engine.py"),
        (r"from\s+app\s+import", "Root app.py was moved to backend/app.py"),
        (r"import\s+app", "Root app.py was moved to backend/app.py"),
        (r"import\s+build_desktop", "build_desktop.py was moved to desktop/build_desktop.py"),
        (r"from\s+build_desktop\s+import", "build_desktop.py was moved to desktop/build_desktop.py"),
    ]
    
    # Walk through all Python files
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                
                # Skip the checker scripts themselves
                if file in ["cleanup.py", "update_readme.py", "check_consistency.py"]:
                    continue
                
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        
                        for pattern, message in patterns:
                            if re.search(pattern, content):
                                print_warning(f"Potential broken import in {file_path}: {message}")
                                issues_found = True
                except Exception as e:
                    print_warning(f"Error reading {file_path}: {str(e)}")
    
    if not issues_found:
        print_success("No potential import issues found")
    
    return issues_found

def check_references():
    """Check for any references to moved files in documentation or scripts"""
    print_status("Checking for references to moved files")
    
    issues_found = False
    
    # Check for references to moved files
    patterns = [
        (r"stegnox_engine\.py", "Root stegnox_engine.py was moved to engine/stegnox_engine.py"),
        (r"app\.py", "Root app.py was moved to backend/app.py"),
        (r"build_desktop\.py", "build_desktop.py was moved to desktop/build_desktop.py"),
        (r"docker-compose\.yml", "docker-compose.yml was moved to deployment/docker-compose.yml"),
        (r"docker-compose\.dev\.yml", "docker-compose.dev.yml was moved to deployment/docker-compose.dev.yml"),
        (r"docker-compose\.prod\.yml", "docker-compose.prod.yml was moved to deployment/docker-compose.prod.yml"),
        (r"deploy\.sh", "deploy.sh was moved to deployment/deploy.sh"),
    ]
    
    # File extensions to check
    extensions = [".md", ".txt", ".sh", ".bat", ".ps1", ".yml", ".yaml"]
    
    # Walk through all documentation and script files
    for root, _, files in os.walk("."):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                
                # Skip the checker scripts themselves
                if file in ["cleanup.py", "update_readme.py", "check_consistency.py"]:
                    continue
                
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        
                        for pattern, message in patterns:
                            if re.search(pattern, content):
                                print_warning(f"Potential reference to moved file in {file_path}: {message}")
                                issues_found = True
                except Exception as e:
                    print_warning(f"Error reading {file_path}: {str(e)}")
    
    if not issues_found:
        print_success("No potential reference issues found")
    
    return issues_found

def check_duplicate_files():
    """Check for any remaining duplicate files"""
    print_status("Checking for duplicate files")
    
    # Map of file names to their paths
    file_map = {}
    duplicate_found = False
    
    # Walk through all files
    for root, _, files in os.walk("."):
        for file in files:
            # Skip the checker scripts themselves
            if file in ["cleanup.py", "update_readme.py", "check_consistency.py"]:
                continue
                
            # Skip common files that might legitimately have the same name
            if file in ["__init__.py", "README.md", "requirements.txt"]:
                continue
                
            if file not in file_map:
                file_map[file] = []
            
            file_map[file].append(os.path.join(root, file))
    
    # Check for duplicates
    for file, paths in file_map.items():
        if len(paths) > 1:
            print_warning(f"Duplicate file found: {file}")
            for path in paths:
                print(f"  - {path}")
            duplicate_found = True
    
    if not duplicate_found:
        print_success("No duplicate files found")
    
    return duplicate_found

def main():
    """Main function to check project consistency"""
    print_status("Starting StegnoX project consistency check")
    
    issues_found = False
    
    # Check for broken imports
    if check_imports():
        issues_found = True
    
    # Check for references to moved files
    if check_references():
        issues_found = True
    
    # Check for duplicate files
    if check_duplicate_files():
        issues_found = True
    
    # Print summary
    if issues_found:
        print_status("Consistency check complete. Issues were found that need to be addressed.")
        print("Please review the warnings above and fix the issues manually.")
    else:
        print_status("Consistency check complete. No issues found!")
        print("The project structure appears to be consistent.")

if __name__ == "__main__":
    main()
