# StegnoX Cleanup Scripts

This directory contains scripts used to clean up the StegnoX project directory structure.

## Scripts

- **cleanup.py**: Removes duplicate files and organizes the directory structure
- **update_readme.py**: Updates the README.md file with the new directory structure
- **check_consistency.py**: Checks for any remaining issues or inconsistencies
- **run_cleanup.py**: Master script that runs all the cleanup scripts in sequence

## Usage

To run the cleanup process:

```bash
cd cleanup
python run_cleanup.py
```

This will:
1. Remove duplicate files in the root directory
2. Create a deployment directory and move deployment-related files there
3. Move build_desktop.py to the desktop directory
4. Update the README.md file with the new directory structure
5. Check for any remaining issues or inconsistencies

## Changes Made

The cleanup process made the following changes to the project structure:

1. **Removed Duplicate Files**:
   - Removed stegnox_engine.py from root (duplicate of engine/stegnox_engine.py)
   - Removed app.py from root (older version of backend/app.py)
   - Removed architecture.md from root (older version of docs/architecture.md)

2. **Organized Deployment Files**:
   - Created a deployment directory
   - Moved deploy.sh to deployment/deploy.sh
   - Moved docker-compose.yml to deployment/docker-compose.yml
   - Moved docker-compose.dev.yml to deployment/docker-compose.dev.yml
   - Moved docker-compose.prod.yml to deployment/docker-compose.prod.yml

3. **Organized Build Scripts**:
   - Moved build_desktop.py to desktop/build_desktop.py

4. **Updated Documentation**:
   - Updated README.md with the new directory structure
   - Updated deployment instructions in README.md

The new directory structure is more organized and follows better project organization practices.
