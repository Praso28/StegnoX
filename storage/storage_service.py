"""
Storage Service for StegnoX

This module handles the storage of images and analysis results.
"""

import os
import json
import uuid
import shutil
import datetime
from PIL import Image
from io import BytesIO

class StorageService:
    def __init__(self, storage_dir="storage"):
        """
        Initialize the storage service

        Args:
            storage_dir (str): Directory to store files
        """
        self.storage_dir = storage_dir
        self.images_dir = os.path.join(storage_dir, "images")
        self.results_dir = os.path.join(storage_dir, "results")
        self.temp_dir = os.path.join(storage_dir, "temp")

        # Create directories if they don't exist
        for directory in [self.storage_dir, self.images_dir, self.results_dir, self.temp_dir]:
            os.makedirs(directory, exist_ok=True)

    def save_image(self, image_data, filename=None):
        """
        Save an image to storage

        Args:
            image_data (bytes or str): The image data or path to image file
            filename (str, optional): The filename to save as. If None, a UUID will be generated.

        Returns:
            str: The path to the saved image
        """
        try:
            # Generate a unique filename if not provided
            if filename is None:
                ext = ".png"  # Default extension
                filename = f"{uuid.uuid4()}{ext}"

            # Ensure the filename has an extension
            if not any(filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']):
                filename += '.png'

            # Create the full path
            image_path = os.path.join(self.images_dir, filename)

            # Handle different input types
            if isinstance(image_data, bytes):
                # Save bytes data directly
                with open(image_path, 'wb') as f:
                    f.write(image_data)
            elif isinstance(image_data, str) and os.path.isfile(image_data):
                # Copy the file if image_data is a file path
                shutil.copy2(image_data, image_path)
            else:
                raise ValueError("image_data must be bytes or a valid file path")

            return image_path

        except Exception as e:
            print(f"Error saving image: {str(e)}")
            return None

    def save_results(self, job_id, results):
        """
        Save analysis results

        Args:
            job_id (str): The job ID
            results (dict): The analysis results

        Returns:
            str: The path to the saved results
        """
        try:
            # Create a filename based on job_id
            if job_id is None:
                job_id = str(uuid.uuid4())

            filename = f"{job_id}.json"
            result_path = os.path.join(self.results_dir, filename)

            # Add timestamp to results
            results_with_meta = {
                "job_id": job_id,
                "timestamp": datetime.datetime.now().isoformat(),
                "results": results
            }

            # Save as JSON
            with open(result_path, 'w') as f:
                json.dump(results_with_meta, f, indent=2)

            return result_path

        except Exception as e:
            print(f"Error saving results: {str(e)}")
            return None

    def get_results(self, job_id):
        """
        Get analysis results

        Args:
            job_id (str): The job ID

        Returns:
            dict: The analysis results or None if not found
        """
        try:
            filename = f"{job_id}.json"
            result_path = os.path.join(self.results_dir, filename)

            if not os.path.exists(result_path):
                return None

            with open(result_path, 'r') as f:
                return json.load(f)

        except Exception as e:
            print(f"Error retrieving results: {str(e)}")
            return None

    def list_results(self, limit=10, offset=0):
        """
        List available results

        Args:
            limit (int): Maximum number of results to return
            offset (int): Offset for pagination

        Returns:
            list: List of result metadata
        """
        try:
            results = []

            # Get all JSON files in the results directory
            result_files = [f for f in os.listdir(self.results_dir) if f.endswith('.json')]

            # Sort by modification time (newest first)
            result_files.sort(key=lambda x: os.path.getmtime(os.path.join(self.results_dir, x)), reverse=True)

            # Apply pagination
            result_files = result_files[offset:offset+limit]

            # Load metadata for each file
            for filename in result_files:
                try:
                    with open(os.path.join(self.results_dir, filename), 'r') as f:
                        data = json.load(f)
                        results.append({
                            "job_id": data.get("job_id"),
                            "timestamp": data.get("timestamp"),
                            "filename": filename
                        })
                except:
                    # Skip files that can't be loaded
                    continue

            return results

        except Exception as e:
            print(f"Error listing results: {str(e)}")
            return []

    def get_image(self, filename):
        """
        Get an image from storage

        Args:
            filename (str): The filename of the image

        Returns:
            bytes: The image data or None if not found
        """
        try:
            image_path = os.path.join(self.images_dir, filename)

            if not os.path.exists(image_path):
                return None

            with open(image_path, 'rb') as f:
                return f.read()

        except Exception as e:
            print(f"Error retrieving image: {str(e)}")
            return None

    def list_images(self, limit=10, offset=0):
        """
        List available images

        Args:
            limit (int): Maximum number of images to return
            offset (int): Offset for pagination

        Returns:
            list: List of image metadata
        """
        try:
            images = []

            # Get all image files in the images directory
            image_files = [f for f in os.listdir(self.images_dir)
                          if any(f.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif'])]

            # Sort by modification time (newest first)
            image_files.sort(key=lambda x: os.path.getmtime(os.path.join(self.images_dir, x)), reverse=True)

            # Apply pagination
            image_files = image_files[offset:offset+limit]

            # Get metadata for each image
            for filename in image_files:
                try:
                    image_path = os.path.join(self.images_dir, filename)
                    stats = os.stat(image_path)

                    # Get image dimensions
                    with Image.open(image_path) as img:
                        width, height = img.size

                    images.append({
                        "filename": filename,
                        "size": stats.st_size,
                        "created": datetime.datetime.fromtimestamp(stats.st_ctime).isoformat(),
                        "modified": datetime.datetime.fromtimestamp(stats.st_mtime).isoformat(),
                        "dimensions": f"{width}x{height}"
                    })
                except:
                    # Skip files that can't be processed
                    continue

            return images

        except Exception as e:
            print(f"Error listing images: {str(e)}")
            return []

    def create_temp_file(self, prefix="temp_", suffix=".tmp"):
        """
        Create a temporary file

        Args:
            prefix (str): Prefix for the filename
            suffix (str): Suffix for the filename

        Returns:
            str: Path to the temporary file
        """
        filename = f"{prefix}{uuid.uuid4()}{suffix}"
        return os.path.join(self.temp_dir, filename)

    def cleanup_temp_files(self, max_age_hours=24):
        """
        Clean up temporary files older than the specified age

        Args:
            max_age_hours (int): Maximum age in hours

        Returns:
            int: Number of files deleted
        """
        try:
            count = 0
            now = datetime.datetime.now()
            max_age = datetime.timedelta(hours=max_age_hours)

            for filename in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, filename)

                if os.path.isfile(file_path):
                    # Get file modification time
                    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

                    # Check if file is older than max_age
                    if now - mtime > max_age:
                        os.remove(file_path)
                        count += 1

            return count

        except Exception as e:
            print(f"Error cleaning up temp files: {str(e)}")
            return 0
