#!/usr/bin/env python3
"""
StegnoX README Update Script

This script updates the README.md file to reflect the new directory structure
after the cleanup process.
"""

import os
import re

def read_file(file_path):
    """Read a file and return its contents"""
    with open(file_path, 'r') as f:
        return f.read()

def write_file(file_path, content):
    """Write content to a file"""
    with open(file_path, 'w') as f:
        f.write(content)

def update_directory_structure(readme_content):
    """Update the directory structure section in the README"""
    # Define the new directory structure
    new_structure = """
```
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
│   └── architecture.md  # System architecture
├── engine/            # Steganography engine
│   ├── stegnox_engine.py  # Core steganography algorithms
│   └── README.md      # Engine documentation
├── examples/          # Example scripts
│   ├── engine_demo.py  # Engine usage examples
│   ├── worker.py      # Worker implementation
│   ├── submit_job.py  # Job submission example
│   └── check_job.py   # Job status checking
├── frontend/          # React web frontend
│   └── src/           # Frontend source code
├── queue/             # Job queue system
│   ├── job_queue.py   # Job queue implementation
│   └── README.md      # Queue documentation
├── storage/           # Storage service
│   ├── storage_service.py  # Storage implementation
│   └── README.md      # Storage documentation
├── tests/             # Test files
│   ├── unit/          # Unit tests
│   ├── integration/   # Integration tests
│   └── e2e/           # End-to-end tests
├── main.py            # Main entry point
├── README.md          # Project documentation
└── requirements.txt   # Python dependencies
```
"""

    # Find the directory structure section and replace it
    pattern = r"```\nStegnoX/\n.*?```"
    updated_content = re.sub(pattern, new_structure.strip(), readme_content, flags=re.DOTALL)
    
    return updated_content

def update_deployment_section(readme_content):
    """Update the deployment section in the README"""
    # Define the new deployment instructions
    new_deployment = """
### Docker Deployment

Deploy using Docker and Docker Compose:

```bash
# Navigate to the deployment directory
cd deployment

# For development
docker-compose -f docker-compose.dev.yml up

# For production
docker-compose -f docker-compose.prod.yml up -d
```

### Desktop Application Distribution

To build the desktop application installers:

```bash
# Navigate to the desktop directory
cd desktop

# Build for all platforms
python build_desktop.py --version 2023.5.1
```
"""

    # Find the deployment section and replace it
    pattern = r"## Deployment.*?```bash\n.*?```"
    updated_content = re.sub(pattern, "## Deployment" + new_deployment, readme_content, flags=re.DOTALL)
    
    return updated_content

def main():
    """Main function to update the README"""
    readme_path = "README.md"
    
    print(f"Updating {readme_path}...")
    
    # Read the current README
    readme_content = read_file(readme_path)
    
    # Create a backup
    backup_path = f"{readme_path}.bak"
    write_file(backup_path, readme_content)
    print(f"Created backup at {backup_path}")
    
    # Update the directory structure
    updated_content = update_directory_structure(readme_content)
    
    # Update the deployment section
    updated_content = update_deployment_section(updated_content)
    
    # Write the updated README
    write_file(readme_path, updated_content)
    print(f"Updated {readme_path} successfully!")
    
    print("\nPlease review the changes to ensure they are correct.")

if __name__ == "__main__":
    main()
