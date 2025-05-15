import os
import pytest
from PIL import Image

@pytest.fixture(scope="session", autouse=True)
def setup_test_data(tmp_path_factory):
    """Create test data directory and sample images"""
    # Create test data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)

    # Create a sample test image
    test_image_path = os.path.join(data_dir, 'test_image.png')
    if not os.path.exists(test_image_path):
        img = Image.new('RGB', (100, 100), color='white')
        img.save(test_image_path)

    return data_dir 