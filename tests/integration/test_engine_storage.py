"""
Integration tests for the StegnoX Engine and Storage Service
"""

import os
import sys
import unittest
import tempfile
import shutil
from PIL import Image

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from engine.stegnox_engine import StegnoxEngine
from storage.storage_service import StorageService

class TestEngineStorageIntegration(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

        # Initialize storage service
        self.storage = StorageService(storage_dir=self.test_dir)

        # Initialize engine
        self.engine = StegnoxEngine()

        # Create a test image
        self.test_image = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        self.test_image.close()
        img = Image.new('RGB', (100, 100), color='white')
        img.save(self.test_image.name)

        # Create a test image with embedded data
        self.stego_image = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        self.stego_image.close()
        self.secret_message = "This is a secret message for testing"
        self.engine.lsb_encoding(self.test_image.name, self.secret_message, self.stego_image.name)

    def tearDown(self):
        # Clean up the test directory
        shutil.rmtree(self.test_dir)

        # Clean up the test images
        if os.path.exists(self.test_image.name):
            os.unlink(self.test_image.name)
        if os.path.exists(self.stego_image.name):
            os.unlink(self.stego_image.name)

    def test_analyze_and_store_results(self):
        """Test analyzing an image and storing the results"""
        # Save the image to storage
        image_path = self.storage.save_image(self.stego_image.name, "test_stego.png")

        # Analyze the image
        results = self.engine.extract_all_methods(image_path)

        # Store the results
        job_id = "test_job_123"
        result_path = self.storage.save_results(job_id, results)

        # Retrieve the results
        retrieved = self.storage.get_results(job_id)

        # Verify the results
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["job_id"], job_id)
        self.assertIn("lsb_extraction", retrieved["results"])
        self.assertIn("parity_bit_extraction", retrieved["results"])
        self.assertIn("metadata_extraction", retrieved["results"])

        # Verify LSB extraction found our message
        lsb_result = retrieved["results"]["lsb_extraction"]
        self.assertIn("message", lsb_result)
        self.assertEqual(lsb_result["message"], self.secret_message)

    def test_encode_and_store_image(self):
        """Test encoding a message and storing the resulting image"""
        # Save the original image to storage
        original_path = self.storage.save_image(self.test_image.name, "test_original.png")

        # Create a temporary file for the output
        output_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        output_file.close()

        # Encode a message
        message = "Another secret message for testing"
        self.engine.lsb_encoding(original_path, message, output_file.name)

        # Save the encoded image to storage
        encoded_path = self.storage.save_image(output_file.name, "test_encoded.png")

        # Verify the encoded image exists
        self.assertTrue(os.path.exists(encoded_path))

        # Decode the message from the stored image
        decoded = self.engine.lsb_extraction(encoded_path)

        # Verify the decoded message
        self.assertIn("message", decoded)
        self.assertEqual(decoded["message"], message)

        # Clean up the output file
        if os.path.exists(output_file.name):
            os.unlink(output_file.name)

    def test_multiple_analysis_methods(self):
        """Test running multiple analysis methods and storing the results"""
        # Save the image to storage
        image_path = self.storage.save_image(self.stego_image.name, "test_multi.png")

        # Run individual analysis methods
        lsb_result = self.engine.lsb_extraction(image_path)
        parity_result = self.engine.parity_bit_extraction(image_path)
        dct_result = self.engine.dct_analysis(image_path)

        # Store the results separately
        job_id = "test_multi_job"
        self.storage.save_results(f"{job_id}_lsb", {"lsb": lsb_result})
        self.storage.save_results(f"{job_id}_parity", {"parity": parity_result})
        self.storage.save_results(f"{job_id}_dct", {"dct": dct_result})

        # Retrieve and verify the results
        lsb_retrieved = self.storage.get_results(f"{job_id}_lsb")
        self.assertIn("lsb", lsb_retrieved["results"])
        self.assertIn("message", lsb_retrieved["results"]["lsb"])

        parity_retrieved = self.storage.get_results(f"{job_id}_parity")
        self.assertIn("parity", parity_retrieved["results"])

        dct_retrieved = self.storage.get_results(f"{job_id}_dct")
        self.assertIn("dct", dct_retrieved["results"])
        self.assertIn("confidence", dct_retrieved["results"]["dct"])

if __name__ == '__main__':
    unittest.main()
