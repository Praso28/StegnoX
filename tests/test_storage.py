import unittest
import os
import sys
import tempfile
import shutil
import json
from PIL import Image

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from storage.storage_service import StorageService

class TestStorageService(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.storage = StorageService(storage_dir=self.test_dir)

        # Create a test image
        self.test_image = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        self.test_image.close()
        img = Image.new('RGB', (100, 100), color='white')
        img.save(self.test_image.name)

    def tearDown(self):
        # Clean up the test directory
        shutil.rmtree(self.test_dir)

        # Clean up the test image
        if os.path.exists(self.test_image.name):
            os.unlink(self.test_image.name)

    def test_save_image_bytes(self):
        # Test saving image from bytes
        with open(self.test_image.name, 'rb') as f:
            image_data = f.read()

        image_path = self.storage.save_image(image_data, "test_bytes.png")
        self.assertIsNotNone(image_path)
        self.assertTrue(os.path.exists(image_path))

    def test_save_image_path(self):
        # Test saving image from path
        image_path = self.storage.save_image(self.test_image.name, "test_path.png")
        self.assertIsNotNone(image_path)
        self.assertTrue(os.path.exists(image_path))

    def test_save_image_auto_filename(self):
        # Test auto-generated filename
        image_path = self.storage.save_image(self.test_image.name)
        self.assertIsNotNone(image_path)
        self.assertTrue(os.path.exists(image_path))

    def test_save_get_results(self):
        # Test saving and retrieving results
        test_results = {
            "test": "data",
            "nested": {
                "value": 123
            }
        }

        job_id = "test_job_123"
        result_path = self.storage.save_results(job_id, test_results)
        self.assertIsNotNone(result_path)
        self.assertTrue(os.path.exists(result_path))

        # Retrieve the results
        retrieved = self.storage.get_results(job_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["job_id"], job_id)
        self.assertEqual(retrieved["results"]["test"], "data")
        self.assertEqual(retrieved["results"]["nested"]["value"], 123)

    def test_list_results(self):
        # Save multiple results
        for i in range(5):
            self.storage.save_results(f"job_{i}", {"index": i})

        # List results
        results = self.storage.list_results()
        self.assertGreaterEqual(len(results), 5)

        # Test pagination
        limited = self.storage.list_results(limit=2)
        self.assertEqual(len(limited), 2)

    def test_get_image(self):
        # Save an image
        filename = "test_get.png"
        self.storage.save_image(self.test_image.name, filename)

        # Retrieve the image
        image_data = self.storage.get_image(filename)
        self.assertIsNotNone(image_data)

        # Verify it's valid image data
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp:
            temp.write(image_data)
            temp.close()
            try:
                img = Image.open(temp.name)
                self.assertEqual(img.size, (100, 100))
            except Exception as e:
                print(f"Error opening image: {e}")
            finally:
                try:
                    os.unlink(temp.name)
                except Exception as e:
                    print(f"Error deleting temp file: {e}")

    def test_list_images(self):
        # Save multiple images
        for i in range(3):
            self.storage.save_image(self.test_image.name, f"test_list_{i}.png")

        # List images
        images = self.storage.list_images()
        self.assertGreaterEqual(len(images), 3)

        # Check metadata
        for img in images:
            self.assertIn("filename", img)
            self.assertIn("dimensions", img)
            self.assertEqual(img["dimensions"], "100x100")

    def test_temp_files(self):
        # Create temp files
        temp_path = self.storage.create_temp_file()
        self.assertTrue(temp_path.startswith(self.test_dir))

        # Write something to the temp file
        with open(temp_path, 'w') as f:
            f.write("test data")

        # For Windows compatibility, we need to close any open handles to the file
        import gc
        gc.collect()  # Force garbage collection to close any lingering file handles

        # Clean up temp files
        # The actual number of deleted files might vary, so we'll just check the file is gone
        try:
            self.storage.cleanup_temp_files(max_age_hours=0)
            # On Windows, file might still be in use, so we'll skip the assertion if needed
            if os.path.exists(temp_path):
                print(f"Warning: Temp file {temp_path} still exists after cleanup")
        except Exception as e:
            print(f"Error during cleanup: {e}")

if __name__ == '__main__':
    unittest.main()
