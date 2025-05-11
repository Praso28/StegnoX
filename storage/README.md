# StegnoX Storage Service

The Storage Service is responsible for managing files and data in the StegnoX application. It provides a unified interface for storing and retrieving images, analysis results, and temporary files.

## Features

- **Image Storage**: Save and retrieve images in various formats
- **Results Storage**: Store and retrieve analysis results in JSON format
- **Temporary File Management**: Create and clean up temporary files
- **Metadata Management**: Track file metadata including creation time, size, and dimensions
- **Pagination Support**: List files with pagination for efficient retrieval

## Directory Structure

The Storage Service organizes files into the following directory structure:

```
storage/
├── images/     # Stores uploaded and processed images
├── results/    # Stores analysis results in JSON format
└── temp/       # Stores temporary files
```

## Usage

### Basic Usage

```python
from storage.storage_service import StorageService

# Create a storage service instance
storage = StorageService(storage_dir="data")

# Save an image
image_path = storage.save_image("path/to/image.png")

# Save analysis results
job_id = "job_123"
results = {"method1": {"message": "Data found"}, "method2": {"message": "No data found"}}
storage.save_results(job_id, results)

# Retrieve results
retrieved_results = storage.get_results(job_id)

# List available images
images = storage.list_images(limit=10, offset=0)

# Clean up temporary files
deleted_count = storage.cleanup_temp_files(max_age_hours=24)
```

### API Reference

#### Image Management

- `save_image(image_data, filename=None)`: Save an image to storage
- `get_image(filename)`: Retrieve an image from storage
- `list_images(limit=10, offset=0)`: List available images with pagination

#### Results Management

- `save_results(job_id, results)`: Save analysis results
- `get_results(job_id)`: Retrieve analysis results
- `list_results(limit=10, offset=0)`: List available results with pagination

#### Temporary File Management

- `create_temp_file(prefix="temp_", suffix=".tmp")`: Create a temporary file
- `cleanup_temp_files(max_age_hours=24)`: Clean up old temporary files

## Development

### Testing

Run the tests to ensure the storage service is working correctly:

```bash
python -m unittest tests/test_storage.py
```

### Adding New Features

When adding new features to the storage service:

1. Add the new method to the `StorageService` class
2. Add appropriate error handling
3. Add tests for the new functionality
4. Update this documentation
