"""
End-to-end tests for the StegnoX web interface
"""

import os
import sys
import unittest
import tempfile
import time
import json
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.app import create_app
from engine.stegnox_engine import StegnoxEngine

class TestWebInterface(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a test image
        cls.test_dir = tempfile.mkdtemp()
        cls.test_image = os.path.join(cls.test_dir, "test_image.png")
        img = Image.new('RGB', (100, 100), color='white')
        img.save(cls.test_image)

        # Create a test image with embedded data
        cls.stego_image = os.path.join(cls.test_dir, "stego_image.png")
        engine = StegnoxEngine()
        cls.secret_message = "This is a secret message for e2e testing"
        engine.lsb_encoding(cls.test_image, cls.secret_message, cls.stego_image)

        # Start the Flask app in testing mode
        cls.app = create_app(testing=True)
        cls.app.config['TESTING'] = True
        cls.app.config['SERVER_NAME'] = 'localhost:5000'
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        # Start the Flask server in a separate thread
        import threading
        def run_app():
            cls.app.run(port=5000)

        cls.server_thread = threading.Thread(target=run_app)
        cls.server_thread.daemon = True
        cls.server_thread.start()

        # Give the server time to start
        time.sleep(1)

        # Set up the Selenium WebDriver
        from selenium.webdriver.chrome.service import Service

        # Use the local ChromeDriver
        service = Service(executable_path='webdrivers/chromedriver.exe')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(service=service, options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        # Clean up
        cls.driver.quit()
        cls.app_context.pop()
        import shutil
        shutil.rmtree(cls.test_dir)

    def test_homepage_loads(self):
        """Test that the homepage loads correctly"""
        self.driver.get('http://localhost:5000')

        # Check that the title is correct
        self.assertIn('StegnoX', self.driver.title)

        # Check that the main elements are present
        self.assertIsNotNone(self.driver.find_element(By.ID, 'navbar'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'footer'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'main-content'))

    def test_image_upload_and_analysis(self):
        """Test uploading an image and analyzing it"""
        self.driver.get('http://localhost:5000/analyze')

        # Upload the image
        file_input = self.driver.find_element(By.ID, 'file-upload')
        file_input.send_keys(self.stego_image)

        # Click the analyze button
        analyze_button = self.driver.find_element(By.ID, 'analyze-button')
        analyze_button.click()

        # Wait for the analysis to complete
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, 'analysis-results'))
        )

        # Check that the results are displayed
        results_element = self.driver.find_element(By.ID, 'analysis-results')
        results_text = results_element.text

        # Verify that the results contain the expected information
        self.assertIn('LSB Extraction', results_text)
        self.assertIn('Parity Bit Extraction', results_text)
        self.assertIn('Metadata Extraction', results_text)
        self.assertIn(self.secret_message, results_text)

    def test_encode_message(self):
        """Test encoding a message into an image"""
        self.driver.get('http://localhost:5000/encode')

        # Upload the image
        file_input = self.driver.find_element(By.ID, 'file-upload')
        file_input.send_keys(self.test_image)

        # Enter a message
        message_input = self.driver.find_element(By.ID, 'message-input')
        test_message = "This is a test message for encoding"
        message_input.send_keys(test_message)

        # Select LSB encoding method
        method_select = self.driver.find_element(By.ID, 'method-select')
        method_select.click()
        lsb_option = self.driver.find_element(By.XPATH, "//option[text()='LSB']")
        lsb_option.click()

        # Click the encode button
        encode_button = self.driver.find_element(By.ID, 'encode-button')
        encode_button.click()

        # Wait for the encoding to complete
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, 'download-link'))
        )

        # Check that the download link is displayed
        download_link = self.driver.find_element(By.ID, 'download-link')
        self.assertTrue(download_link.is_displayed())

    def test_job_management(self):
        """Test job management functionality"""
        # First, upload and analyze an image to create a job
        self.driver.get('http://localhost:5000/analyze')
        file_input = self.driver.find_element(By.ID, 'file-upload')
        file_input.send_keys(self.stego_image)
        analyze_button = self.driver.find_element(By.ID, 'analyze-button')
        analyze_button.click()

        # Wait for the analysis to complete
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, 'analysis-results'))
        )

        # Go to the jobs page
        self.driver.get('http://localhost:5000/jobs')

        # Wait for the jobs to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'job-item'))
        )

        # Check that at least one job is displayed
        job_items = self.driver.find_elements(By.CLASS_NAME, 'job-item')
        self.assertGreaterEqual(len(job_items), 1)

        # Click on the first job to view details
        job_items[0].click()

        # Wait for the job details to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'job-details'))
        )

        # Check that the job details are displayed
        job_details = self.driver.find_element(By.ID, 'job-details')
        details_text = job_details.text

        # Verify that the details contain the expected information
        self.assertIn('Job ID', details_text)
        self.assertIn('Status', details_text)
        self.assertIn('COMPLETED', details_text)
        self.assertIn('Results', details_text)

if __name__ == '__main__':
    unittest.main()
