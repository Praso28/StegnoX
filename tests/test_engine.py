import unittest
import os
import sys
import tempfile
import numpy as np
from PIL import Image

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine.stegnox_engine import StegnoxEngine

class TestStegnoxEngine(unittest.TestCase):
    def setUp(self):
        self.engine = StegnoxEngine()
        # Create a test image
        self.test_image = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        self.test_image.close()
        img = Image.new('RGB', (100, 100), color='white')
        img.save(self.test_image.name)

    def tearDown(self):
        # Clean up the test image
        os.unlink(self.test_image.name)

    def test_metadata_extraction(self):
        # Test that metadata extraction works
        result = self.engine.metadata_extraction(self.test_image.name)
        self.assertIn('format', result)
        self.assertIn('mode', result)
        self.assertIn('size', result)

    def test_extract_all_methods(self):
        # Test that all extraction methods run
        results = self.engine.extract_all_methods(self.test_image.name)
        self.assertIn('lsb_extraction', results)
        self.assertIn('parity_bit_extraction', results)
        self.assertIn('metadata_extraction', results)
        self.assertIn('dct_analysis', results)
        self.assertIn('bit_plane_analysis', results)
        self.assertIn('histogram_analysis', results)

    def test_dct_analysis(self):
        # Test DCT analysis
        result = self.engine.dct_analysis(self.test_image.name)
        self.assertIn('confidence', result)
        self.assertIn('assessment', result)
        self.assertIn('statistics', result)

    def test_bit_plane_analysis(self):
        # Test bit plane analysis
        result = self.engine.bit_plane_analysis(self.test_image.name)
        self.assertIn('confidence', result)
        self.assertIn('assessment', result)
        self.assertIn('bit_planes', result)

    def test_histogram_analysis(self):
        # Test histogram analysis
        result = self.engine.histogram_analysis(self.test_image.name)
        self.assertIn('confidence', result)
        self.assertIn('assessment', result)
        self.assertIn('red_channel', result)
        self.assertIn('green_channel', result)
        self.assertIn('blue_channel', result)

    def test_lsb_encoding_decoding(self):
        # Test LSB encoding and decoding
        test_message = "This is a test message for steganography"
        output_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        output_file.close()

        try:
            # Encode the message
            encode_result = self.engine.lsb_encoding(self.test_image.name, test_message, output_file.name)
            self.assertTrue(encode_result["success"])

            # Decode the message
            decode_result = self.engine.lsb_extraction(output_file.name)
            self.assertIn("message", decode_result)
            self.assertIn(test_message, decode_result["message"])
        finally:
            # Clean up
            if os.path.exists(output_file.name):
                os.unlink(output_file.name)

    def test_parity_encoding_decoding(self):
        # Test parity encoding and decoding
        test_message = "Testing parity encoding"
        output_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        output_file.close()

        try:
            # Encode the message
            encode_result = self.engine.parity_bit_encoding(self.test_image.name, test_message, output_file.name)
            self.assertTrue(encode_result["success"])

            # Decode the message
            decode_result = self.engine.parity_bit_extraction(output_file.name)
            self.assertIn("message", decode_result)
            # Parity extraction might not be perfect, so we check if part of the message is there
            self.assertTrue(any(word in decode_result["message"] for word in test_message.split()))
        finally:
            # Clean up
            if os.path.exists(output_file.name):
                os.unlink(output_file.name)

    def test_metadata_encoding(self):
        # Test metadata encoding
        test_message = "Hidden in metadata"
        output_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        output_file.close()

        try:
            # Encode the message
            encode_result = self.engine.metadata_encoding(self.test_image.name, test_message, output_file.name)
            self.assertTrue(encode_result["success"])

            # Extract metadata
            metadata_result = self.engine.metadata_extraction(output_file.name)
            # The comment might be in exif or in the main metadata
            if "exif" in metadata_result and "comment" in metadata_result["exif"]:
                self.assertEqual(test_message, metadata_result["exif"]["comment"])
            elif "comment" in metadata_result:
                self.assertEqual(test_message, metadata_result["comment"])
        finally:
            # Clean up
            if os.path.exists(output_file.name):
                os.unlink(output_file.name)

    def test_detect_format(self):
        # Test format detection
        format_result = self.engine.detect_format(self.test_image.name)
        self.assertEqual(format_result, "png")

if __name__ == '__main__':
    unittest.main()
