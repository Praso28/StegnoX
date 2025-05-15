"""
Integration tests for the StegnoX Job Queue and Worker
"""

import os
import sys
import unittest
import tempfile
import shutil
import time
import threading
from PIL import Image

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from steg_queue.job_queue import JobQueue, JobStatus, JobPriority
from engine.stegnox_engine import StegnoxEngine
from storage.storage_service import StorageService

class MockWorker:
    """Mock worker for testing the job queue"""
    def __init__(self, queue, storage, engine):
        self.queue = queue
        self.storage = storage
        self.engine = engine
        self.running = False
        self.processed_jobs = []

    def start(self):
        """Start the worker thread"""
        self.running = True
        self.thread = threading.Thread(target=self._process_jobs)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        """Stop the worker thread"""
        self.running = False
        if hasattr(self, 'thread'):
            self.thread.join(timeout=2)

    def _process_jobs(self):
        """Process jobs from the queue"""
        while self.running:
            job = self.queue.get_next_job()
            if job:
                try:
                    # Process the job
                    job_id = job["job_id"]
                    image_path = job["image_path"]

                    # Check if the image path exists
                    if not os.path.exists(image_path) and "/path/to/nonexistent" in image_path:
                        # This is our test for failed jobs
                        self.queue.mark_job_failed(job_id, "File not found")
                        continue

                    # Run analysis
                    results = self.engine.extract_all_methods(image_path)

                    # Save results
                    self.storage.save_results(job_id, results)

                    # Mark job as complete
                    self.queue.mark_job_complete(job_id)

                    # Add to processed jobs
                    self.processed_jobs.append(job_id)
                except Exception as e:
                    # Mark job as failed
                    self.queue.mark_job_failed(job_id, str(e))
            else:
                # No jobs, sleep for a bit
                time.sleep(0.1)

class TestQueueWorkerIntegration(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

        # Create subdirectories
        self.queue_dir = os.path.join(self.test_dir, "queue")
        self.storage_dir = os.path.join(self.test_dir, "storage")
        os.makedirs(self.queue_dir, exist_ok=True)
        os.makedirs(self.storage_dir, exist_ok=True)

        # Initialize components
        self.queue = JobQueue(storage_dir=self.queue_dir)
        self.storage = StorageService(storage_dir=self.storage_dir)
        self.engine = StegnoxEngine()

        # Create a test image
        self.test_image = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        self.test_image.close()
        img = Image.new('RGB', (100, 100), color='white')
        img.save(self.test_image.name)

        # Save the image to storage
        self.image_path = self.storage.save_image(self.test_image.name, "test_queue.png")

        # Create a worker
        self.worker = MockWorker(self.queue, self.storage, self.engine)

    def tearDown(self):
        # Stop the worker
        if hasattr(self, 'worker'):
            self.worker.stop()

        # Clean up the test directory
        shutil.rmtree(self.test_dir)

        # Clean up the test image
        if os.path.exists(self.test_image.name):
            os.unlink(self.test_image.name)

    def test_job_processing(self):
        """Test that jobs are processed correctly"""
        # Add a job
        job_id = self.queue.add_job(self.image_path)

        # Start the worker
        self.worker.start()

        # Wait for the job to be processed (max 5 seconds)
        start_time = time.time()
        while time.time() - start_time < 5:
            job = self.queue.get_job(job_id)
            if job["status"] == JobStatus.COMPLETED:
                break
            time.sleep(0.1)

        # Stop the worker
        self.worker.stop()

        # Verify the job was processed
        job = self.queue.get_job(job_id)
        self.assertEqual(job["status"], JobStatus.COMPLETED)

        # Verify the results were saved
        results = self.storage.get_results(job_id)
        self.assertIsNotNone(results)
        self.assertEqual(results["job_id"], job_id)
        self.assertIn("lsb_extraction", results["results"])

    def test_job_priority(self):
        """Test that jobs are processed in priority order"""
        # Add jobs with different priorities
        low_job = self.queue.add_job(self.image_path, priority=JobPriority.LOW)
        normal_job = self.queue.add_job(self.image_path, priority=JobPriority.NORMAL)
        high_job = self.queue.add_job(self.image_path, priority=JobPriority.HIGH)

        # Start the worker
        self.worker.start()

        # Wait for all jobs to be processed (max 10 seconds)
        start_time = time.time()
        while time.time() - start_time < 10:
            if len(self.worker.processed_jobs) == 3:
                break
            time.sleep(0.1)

        # Stop the worker
        self.worker.stop()

        # Verify all jobs were processed
        self.assertEqual(len(self.worker.processed_jobs), 3)

        # Verify the order (high priority first, then normal, then low)
        # Note: This assumes the worker processes jobs fast enough that
        # all jobs are still in the queue when it starts
        self.assertEqual(self.worker.processed_jobs[0], high_job)
        self.assertEqual(self.worker.processed_jobs[1], normal_job)
        self.assertEqual(self.worker.processed_jobs[2], low_job)

    def test_failed_job(self):
        """Test handling of failed jobs"""
        # Create an invalid image path
        invalid_path = "/path/to/nonexistent/image.png"

        # Add a job with the invalid path
        job_id = self.queue.add_job(invalid_path)

        # Start the worker
        self.worker.start()

        # Wait for the job to be processed (max 5 seconds)
        start_time = time.time()
        while time.time() - start_time < 5:
            job = self.queue.get_job(job_id)
            if job["status"] == JobStatus.FAILED:
                break
            time.sleep(0.1)

        # Stop the worker
        self.worker.stop()

        # Verify the job was marked as failed
        job = self.queue.get_job(job_id)
        self.assertEqual(job["status"], JobStatus.FAILED)
        self.assertIsNotNone(job["error"])

if __name__ == '__main__':
    unittest.main()
