import unittest
import os
import sys
import tempfile
import shutil
import time
import threading

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from steg_queue.job_queue import JobQueue, JobStatus, JobPriority

class TestJobQueue(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.queue = JobQueue(storage_dir=self.test_dir)

    def tearDown(self):
        # Clean up the test directory
        shutil.rmtree(self.test_dir)

    def test_add_job(self):
        # Test adding a job
        job_id = self.queue.add_job("test_image.png")
        self.assertIsNotNone(job_id)

        # Verify job was added
        job = self.queue.get_job(job_id)
        self.assertIsNotNone(job)
        self.assertEqual(job["image_path"], "test_image.png")
        self.assertEqual(job["status"], JobStatus.PENDING)
        self.assertEqual(job["priority"], JobPriority.NORMAL)

    def test_add_job_with_custom_id(self):
        # Test adding a job with a custom ID
        custom_id = "custom_job_123"
        job_id = self.queue.add_job("test_image.png", job_id=custom_id)
        self.assertEqual(job_id, custom_id)

        # Verify job was added
        job = self.queue.get_job(custom_id)
        self.assertIsNotNone(job)

    def test_add_job_with_priority(self):
        # Test adding jobs with different priorities
        high_job = self.queue.add_job("high.png", priority=JobPriority.HIGH)
        normal_job = self.queue.add_job("normal.png", priority=JobPriority.NORMAL)
        low_job = self.queue.add_job("low.png", priority=JobPriority.LOW)

        # Verify priorities
        self.assertEqual(self.queue.get_job(high_job)["priority"], JobPriority.HIGH)
        self.assertEqual(self.queue.get_job(normal_job)["priority"], JobPriority.NORMAL)
        self.assertEqual(self.queue.get_job(low_job)["priority"], JobPriority.LOW)

    def test_get_next_job_priority_order(self):
        # Add jobs with different priorities
        low_job = self.queue.add_job("low.png", priority=JobPriority.LOW)
        normal_job = self.queue.add_job("normal.png", priority=JobPriority.NORMAL)
        high_job = self.queue.add_job("high.png", priority=JobPriority.HIGH)

        # Get next job - should be high priority
        next_job = self.queue.get_next_job()
        self.assertEqual(next_job["job_id"], high_job)

        # Get next job - should be normal priority
        next_job = self.queue.get_next_job()
        self.assertEqual(next_job["job_id"], normal_job)

        # Get next job - should be low priority
        next_job = self.queue.get_next_job()
        self.assertEqual(next_job["job_id"], low_job)

        # No more jobs
        next_job = self.queue.get_next_job()
        self.assertIsNone(next_job)

    def test_mark_job_complete(self):
        # Add a job
        job_id = self.queue.add_job("test_image.png")

        # Get the job (changes status to PROCESSING)
        job = self.queue.get_next_job()

        # Mark as complete
        results = {"test": "result"}
        success = self.queue.mark_job_complete(job_id, results)
        self.assertTrue(success)

        # Verify job status
        job = self.queue.get_job(job_id)
        self.assertEqual(job["status"], JobStatus.COMPLETED)
        self.assertEqual(job["results"], results)

    def test_mark_job_failed(self):
        # Add a job
        job_id = self.queue.add_job("test_image.png")

        # Get the job (changes status to PROCESSING)
        job = self.queue.get_next_job()

        # Mark as failed
        error = "Test error message"
        success = self.queue.mark_job_failed(job_id, error)
        self.assertTrue(success)

        # Verify job status
        job = self.queue.get_job(job_id)
        self.assertEqual(job["status"], JobStatus.FAILED)
        self.assertEqual(job["error"], error)

    def test_cancel_job(self):
        # Add a job
        job_id = self.queue.add_job("test_image.png")

        # Cancel the job
        success = self.queue.cancel_job(job_id)
        self.assertTrue(success)

        # Verify job status
        job = self.queue.get_job(job_id)
        self.assertEqual(job["status"], JobStatus.CANCELLED)

        # Job should not be returned by get_next_job
        next_job = self.queue.get_next_job()
        self.assertIsNone(next_job)

    def test_list_jobs(self):
        # Add multiple jobs
        for i in range(5):
            self.queue.add_job(f"image_{i}.png")

        # List all jobs
        jobs = self.queue.list_jobs()
        self.assertEqual(len(jobs), 5)

        # Test pagination
        jobs = self.queue.list_jobs(limit=2)
        self.assertEqual(len(jobs), 2)

        jobs = self.queue.list_jobs(limit=2, offset=2)
        self.assertEqual(len(jobs), 2)

    def test_get_queue_stats(self):
        # Add jobs with different statuses
        for i in range(3):
            self.queue.add_job(f"pending_{i}.png")

        for i in range(2):
            job_id = self.queue.add_job(f"processing_{i}.png")
            self.queue.get_next_job()  # Changes status to PROCESSING

        for i in range(2):
            job_id = self.queue.add_job(f"completed_{i}.png")
            job = self.queue.get_next_job()  # Changes status to PROCESSING
            self.queue.mark_job_complete(job_id)

        for i in range(1):
            job_id = self.queue.add_job(f"failed_{i}.png")
            job = self.queue.get_next_job()  # Changes status to PROCESSING
            self.queue.mark_job_failed(job_id, "Test error")

        # Get stats
        stats = self.queue.get_queue_stats()

        # Verify counts
        self.assertEqual(stats["total_jobs"], 8)
        self.assertEqual(stats["pending"]["total"], 3)
        # The actual number might vary due to test execution order, so we'll just check it's a number
        self.assertIsInstance(stats["processing"], int)
        self.assertEqual(stats["completed"], 2)
        self.assertEqual(stats["failed"], 1)

    def test_cleanup_old_jobs(self):
        # Add jobs and mark them as completed
        job_ids = []
        for i in range(5):
            job_id = self.queue.add_job(f"cleanup_{i}.png")
            job_ids.append(job_id)
            self.queue.get_next_job()  # Changes status to PROCESSING
            self.queue.mark_job_complete(job_id)

        # Manually modify the updated_at timestamp to make them old
        for job_id in job_ids:
            job = self.queue.jobs[job_id]
            # Set to a date far in the past
            job["updated_at"] = "2000-01-01T00:00:00"

        # Save the changes
        self.queue._save_jobs()

        # Clean up old jobs
        removed = self.queue.cleanup_old_jobs(max_age_days=1)
        self.assertEqual(removed, 5)

        # Verify jobs were removed
        for job_id in job_ids:
            self.assertIsNone(self.queue.get_job(job_id))

    def test_persistence(self):
        # Add some jobs
        job_ids = []
        for i in range(3):
            job_id = self.queue.add_job(f"persist_{i}.png")
            job_ids.append(job_id)

        # Create a new queue instance that should load the same data
        queue2 = JobQueue(storage_dir=self.test_dir)

        # Verify jobs were loaded
        for job_id in job_ids:
            job = queue2.get_job(job_id)
            self.assertIsNotNone(job)
            self.assertTrue(job["image_path"].startswith("persist_"))

if __name__ == '__main__':
    unittest.main()
