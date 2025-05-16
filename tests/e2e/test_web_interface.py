"""
End-to-end tests for the StegnoX web interface
"""

import os
import sys
import tempfile
import time
import json
import pytest
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from engine.stegnox_engine import StegnoxEngine

@pytest.fixture(scope='session')
def test_images():
    """Create test images for the session"""
    test_dir = tempfile.mkdtemp()
    test_image = os.path.join(test_dir, "test_image.png")
    stego_image = os.path.join(test_dir, "stego_image.png")
    
    # Create a test image
    img = Image.new('RGB', (100, 100), color='white')
    img.save(test_image)
    
    # Create a test image with embedded data
    engine = StegnoxEngine()
    secret_message = "This is a secret message for e2e testing"
    engine.lsb_encoding(test_image, secret_message, stego_image)
    
    yield {
        'dir': test_dir,
        'clean': test_image,
        'stego': stego_image,
        'secret_message': secret_message
    }
    
    # Cleanup
    import shutil
    shutil.rmtree(test_dir)

@pytest.fixture(scope='session')
def driver():
    """Set up and return a Selenium WebDriver"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Use webdriver_manager to handle driver installation
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()

@pytest.fixture(scope='session', autouse=True)
def app_server(app):
    """Start the Flask server for testing"""
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost:5000'
    
    # Start the Flask server in a separate thread
    import threading
    def run_app():
        app.run(port=5000)

    server_thread = threading.Thread(target=run_app)
    server_thread.daemon = True
    server_thread.start()
    
    # Give the server time to start
    time.sleep(1)
    
    yield app

def test_homepage_loads(driver):
    """Test that the homepage loads correctly"""
    driver.get('http://localhost:5000')

    # Check that the title is correct
    assert 'StegnoX' in driver.title

    # Check that the main elements are present
    assert driver.find_element(By.ID, 'navbar') is not None
    assert driver.find_element(By.ID, 'footer') is not None
    assert driver.find_element(By.ID, 'main-content') is not None

def test_image_upload_and_analysis(driver, test_images):
    """Test uploading an image and analyzing it"""
    driver.get('http://localhost:5000/analyze')

    # Upload the image
    file_input = driver.find_element(By.ID, 'file-upload')
    file_input.send_keys(test_images['stego'])

    # Click the analyze button
    analyze_button = driver.find_element(By.ID, 'analyze-button')
    analyze_button.click()

    # Wait for the analysis to complete
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'analysis-results'))
    )

    # Check that the results are displayed
    results_element = driver.find_element(By.ID, 'analysis-results')
    results_text = results_element.text

    # Verify that the results contain the expected information
    assert 'LSB Extraction' in results_text
    assert 'Parity Bit Extraction' in results_text
    assert 'Metadata Extraction' in results_text
    assert test_images['secret_message'] in results_text

def test_encode_message(driver, test_images):
    """Test encoding a message into an image"""
    driver.get('http://localhost:5000/encode')

    # Upload the image
    file_input = driver.find_element(By.ID, 'file-upload')
    file_input.send_keys(test_images['clean'])

    # Enter a message
    message_input = driver.find_element(By.ID, 'message-input')
    test_message = "This is a test message for encoding"
    message_input.send_keys(test_message)

    # Select LSB encoding method
    method_select = driver.find_element(By.ID, 'method-select')
    method_select.click()
    lsb_option = driver.find_element(By.XPATH, "//option[text()='LSB']")
    lsb_option.click()

    # Click the encode button
    encode_button = driver.find_element(By.ID, 'encode-button')
    encode_button.click()

    # Wait for the encoding to complete
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'download-link'))
    )

    # Check that the download link is displayed
    download_link = driver.find_element(By.ID, 'download-link')
    assert download_link.is_displayed()

def test_job_management(driver, test_images):
    """Test job management functionality"""
    # First, upload and analyze an image to create a job
    driver.get('http://localhost:5000/analyze')
    file_input = driver.find_element(By.ID, 'file-upload')
    file_input.send_keys(test_images['stego'])
    analyze_button = driver.find_element(By.ID, 'analyze-button')
    analyze_button.click()

    # Wait for the analysis to complete
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'analysis-results'))
    )

    # Go to the jobs page
    driver.get('http://localhost:5000/jobs')

    # Wait for the jobs to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'job-item'))
    )

    # Check that at least one job is displayed
    job_items = driver.find_elements(By.CLASS_NAME, 'job-item')
    assert len(job_items) >= 1

    # Click on the first job to view details
    job_items[0].click()

    # Wait for the job details to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'job-details'))
    )

    # Check that the job details are displayed
    job_details = driver.find_element(By.ID, 'job-details')
    details_text = job_details.text

    # Verify that the details contain the expected information
    assert 'Job ID' in details_text
    assert 'Status' in details_text
    assert 'COMPLETED' in details_text
    assert 'Results' in details_text
