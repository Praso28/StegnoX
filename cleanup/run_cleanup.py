#!/usr/bin/env python3
"""
StegnoX Project Cleanup Master Script

This script runs all the cleanup scripts in sequence:
1. cleanup.py - Removes duplicate files and organizes the directory structure
2. update_readme.py - Updates the README.md file with the new directory structure
3. check_consistency.py - Checks for any remaining issues or inconsistencies
"""

import os
import sys
import subprocess
import time

def print_header(message):
    """Print a header message with formatting"""
    print("\n" + "=" * 80)
    print(f" {message} ".center(80, "="))
    print("=" * 80 + "\n")

def run_script(script_name):
    """Run a Python script and return its exit code"""
    print_header(f"Running {script_name}")
    
    try:
        result = subprocess.run([sys.executable, script_name], check=False)
        return result.returncode
    except Exception as e:
        print(f"Error running {script_name}: {str(e)}")
        return 1

def main():
    """Main function to run all cleanup scripts"""
    print_header("StegnoX Project Cleanup")
    print("This script will clean up the StegnoX project directory structure.")
    print("It will remove duplicate files, organize configuration files,")
    print("update the README.md file, and check for any remaining issues.")
    print("\nMake sure you have a backup of your project before proceeding!")
    
    # Ask for confirmation
    response = input("\nDo you want to proceed? (y/n): ")
    if response.lower() != 'y':
        print("Cleanup aborted.")
        return
    
    # Run cleanup.py
    cleanup_exit_code = run_script("cleanup.py")
    if cleanup_exit_code != 0:
        print("\nWarning: cleanup.py exited with non-zero status.")
        response = input("Do you want to continue with the next script? (y/n): ")
        if response.lower() != 'y':
            print("Cleanup process aborted.")
            return
    
    # Run update_readme.py
    readme_exit_code = run_script("update_readme.py")
    if readme_exit_code != 0:
        print("\nWarning: update_readme.py exited with non-zero status.")
        response = input("Do you want to continue with the next script? (y/n): ")
        if response.lower() != 'y':
            print("Cleanup process aborted.")
            return
    
    # Run check_consistency.py
    consistency_exit_code = run_script("check_consistency.py")
    
    # Print summary
    print_header("Cleanup Summary")
    print(f"cleanup.py: {'Success' if cleanup_exit_code == 0 else 'Warning (see above)'}")
    print(f"update_readme.py: {'Success' if readme_exit_code == 0 else 'Warning (see above)'}")
    print(f"check_consistency.py: {'Success' if consistency_exit_code == 0 else 'Issues found (see above)'}")
    
    if cleanup_exit_code == 0 and readme_exit_code == 0 and consistency_exit_code == 0:
        print("\nAll cleanup tasks completed successfully!")
    else:
        print("\nCleanup completed with warnings or issues.")
        print("Please review the output above and address any remaining issues manually.")
    
    print("\nNext steps:")
    print("1. Review the updated README.md file")
    print("2. Fix any issues reported by check_consistency.py")
    print("3. Test the application to ensure everything still works")
    print("4. Commit the changes to version control")

if __name__ == "__main__":
    main()
