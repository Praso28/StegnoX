"""
Job Queue System for StegnoX

This module handles the queuing of steganography analysis jobs.
"""

import os
import uuid
import json
import time
import threading
import datetime
from enum import Enum
from collections import deque

class JobStatus(Enum):
    """Job status enum"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class JobPriority(Enum):
    """Job priority enum"""
    LOW = 0
    NORMAL = 1
    HIGH = 2

class JobQueue:
    def __init__(self, storage_dir="queue"):
        """
        Initialize the job queue

        Args:
            storage_dir (str): Directory to store job data
        """
        self.jobs = {}  # Dictionary of all jobs by ID
        self.pending_jobs = {
            JobPriority.LOW: deque(),
            JobPriority.NORMAL: deque(),
            JobPriority.HIGH: deque()
        }
        self.processing_jobs = {}
        self.completed_jobs = {}
        self.failed_jobs = {}

        self.storage_dir = storage_dir
        self.jobs_file = os.path.join(storage_dir, "jobs.json")

        # Create storage directory if it doesn't exist
        os.makedirs(storage_dir, exist_ok=True)

        # Load existing jobs if available
        self._load_jobs()

        # Lock for thread safety
        self.lock = threading.RLock()

        # Start background thread for auto-saving jobs
        self.autosave_interval = 60  # seconds
        self.autosave_thread = threading.Thread(target=self._autosave_worker, daemon=True)
        self.autosave_thread.start()

    def _autosave_worker(self):
        """Background thread for auto-saving jobs"""
        while True:
            time.sleep(self.autosave_interval)
            try:
                self._save_jobs()
            except Exception as e:
                print(f"Error in autosave: {str(e)}")

    def _save_jobs(self):
        """Save jobs to disk"""
        with self.lock:
            # Convert jobs to serializable format
            serializable_jobs = {}
            for job_id, job in self.jobs.items():
                serializable_job = job.copy()
                # Convert enum values to strings
                serializable_job["status"] = serializable_job["status"].value
                serializable_job["priority"] = serializable_job["priority"].value
                serializable_jobs[job_id] = serializable_job

            # Save to file
            with open(self.jobs_file, 'w') as f:
                json.dump(serializable_jobs, f, indent=2)

    def _load_jobs(self):
        """Load jobs from disk"""
        if not os.path.exists(self.jobs_file):
            return

        try:
            with open(self.jobs_file, 'r') as f:
                serializable_jobs = json.load(f)

            # Convert back to internal format
            for job_id, job in serializable_jobs.items():
                # Convert string values back to enums
                job["status"] = JobStatus(job["status"])
                job["priority"] = JobPriority(job["priority"])

                # Add to appropriate collections
                self.jobs[job_id] = job

                if job["status"] == JobStatus.PENDING:
                    self.pending_jobs[job["priority"]].append(job_id)
                elif job["status"] == JobStatus.PROCESSING:
                    self.processing_jobs[job_id] = job
                elif job["status"] == JobStatus.COMPLETED:
                    self.completed_jobs[job_id] = job
                elif job["status"] == JobStatus.FAILED:
                    self.failed_jobs[job_id] = job
        except Exception as e:
            print(f"Error loading jobs: {str(e)}")

    def add_job(self, image_path, job_id=None, priority=JobPriority.NORMAL, metadata=None):
        """
        Add a new job to the queue

        Args:
            image_path (str): Path to the image to analyze
            job_id (str, optional): Custom job ID. If None, one will be generated.
            priority (JobPriority): Job priority
            metadata (dict, optional): Additional metadata for the job

        Returns:
            str: The job ID
        """
        with self.lock:
            # Generate job ID if not provided
            if job_id is None:
                job_id = str(uuid.uuid4())

            # Create job object
            job = {
                "job_id": job_id,
                "image_path": image_path,
                "status": JobStatus.PENDING,
                "priority": priority,
                "created_at": datetime.datetime.now().isoformat(),
                "updated_at": datetime.datetime.now().isoformat(),
                "metadata": metadata or {}
            }

            # Add to collections
            self.jobs[job_id] = job
            self.pending_jobs[priority].append(job_id)

            # Save to disk
            self._save_jobs()

            return job_id

    def get_next_job(self, worker_id=None):
        """
        Get the next job from the queue

        Args:
            worker_id (str, optional): ID of the worker requesting the job

        Returns:
            dict: Job information or None if queue is empty
        """
        with self.lock:
            # Check high priority jobs first, then normal, then low
            for priority in [JobPriority.HIGH, JobPriority.NORMAL, JobPriority.LOW]:
                if self.pending_jobs[priority]:
                    job_id = self.pending_jobs[priority].popleft()
                    job = self.jobs[job_id]

                    # Update job status
                    job["status"] = JobStatus.PROCESSING
                    job["updated_at"] = datetime.datetime.now().isoformat()
                    job["started_at"] = datetime.datetime.now().isoformat()
                    if worker_id:
                        job["worker_id"] = worker_id

                    # Move to processing collection
                    self.processing_jobs[job_id] = job

                    # Save changes
                    self._save_jobs()

                    return job

            # No jobs available
            return None

    def mark_job_complete(self, job_id, results=None):
        """
        Mark a job as complete with results

        Args:
            job_id (str): The job ID
            results (dict, optional): The analysis results

        Returns:
            bool: Success status
        """
        with self.lock:
            if job_id not in self.jobs:
                return False

            job = self.jobs[job_id]

            # Update job status
            job["status"] = JobStatus.COMPLETED
            job["updated_at"] = datetime.datetime.now().isoformat()
            job["completed_at"] = datetime.datetime.now().isoformat()

            if results:
                job["results"] = results

            # Move to completed collection
            if job_id in self.processing_jobs:
                del self.processing_jobs[job_id]
            self.completed_jobs[job_id] = job

            # Save changes
            self._save_jobs()

            return True

    def mark_job_failed(self, job_id, error=None):
        """
        Mark a job as failed

        Args:
            job_id (str): The job ID
            error (str, optional): Error message

        Returns:
            bool: Success status
        """
        with self.lock:
            if job_id not in self.jobs:
                return False

            job = self.jobs[job_id]

            # Update job status
            job["status"] = JobStatus.FAILED
            job["updated_at"] = datetime.datetime.now().isoformat()
            job["failed_at"] = datetime.datetime.now().isoformat()

            if error:
                job["error"] = error

            # Move to failed collection
            if job_id in self.processing_jobs:
                del self.processing_jobs[job_id]
            self.failed_jobs[job_id] = job

            # Save changes
            self._save_jobs()

            return True

    def cancel_job(self, job_id):
        """
        Cancel a pending job

        Args:
            job_id (str): The job ID

        Returns:
            bool: Success status
        """
        with self.lock:
            if job_id not in self.jobs:
                return False

            job = self.jobs[job_id]

            # Can only cancel pending jobs
            if job["status"] != JobStatus.PENDING:
                return False

            # Update job status
            job["status"] = JobStatus.CANCELLED
            job["updated_at"] = datetime.datetime.now().isoformat()

            # Remove from pending queue
            priority = job["priority"]
            try:
                self.pending_jobs[priority].remove(job_id)
            except ValueError:
                # Job not in queue (shouldn't happen)
                pass

            # Save changes
            self._save_jobs()

            return True

    def get_job(self, job_id):
        """
        Get job information

        Args:
            job_id (str): The job ID

        Returns:
            dict: Job information or None if not found
        """
        with self.lock:
            return self.jobs.get(job_id)

    def list_jobs(self, status=None, limit=10, offset=0):
        """
        List jobs with optional filtering

        Args:
            status (JobStatus, optional): Filter by status
            limit (int): Maximum number of jobs to return
            offset (int): Offset for pagination

        Returns:
            list: List of job information
        """
        with self.lock:
            # Filter jobs by status if specified
            if status:
                filtered_jobs = [job for job in self.jobs.values() if job["status"] == status]
            else:
                filtered_jobs = list(self.jobs.values())

            # Sort by creation time (newest first)
            filtered_jobs.sort(key=lambda x: x["created_at"], reverse=True)

            # Apply pagination
            paginated_jobs = filtered_jobs[offset:offset+limit]

            return paginated_jobs

    def get_queue_stats(self):
        """
        Get statistics about the job queue

        Returns:
            dict: Queue statistics
        """
        with self.lock:
            return {
                "total_jobs": len(self.jobs),
                "pending": {
                    "total": sum(len(q) for q in self.pending_jobs.values()),
                    "high_priority": len(self.pending_jobs[JobPriority.HIGH]),
                    "normal_priority": len(self.pending_jobs[JobPriority.NORMAL]),
                    "low_priority": len(self.pending_jobs[JobPriority.LOW])
                },
                "processing": len(self.processing_jobs),
                "completed": len(self.completed_jobs),
                "failed": len(self.failed_jobs)
            }

    def cleanup_old_jobs(self, max_age_days=30):
        """
        Remove old completed and failed jobs

        Args:
            max_age_days (int): Maximum age in days

        Returns:
            int: Number of jobs removed
        """
        with self.lock:
            count = 0
            now = datetime.datetime.now()
            max_age = datetime.timedelta(days=max_age_days)

            # Find old jobs to remove
            jobs_to_remove = []

            for job_id, job in list(self.jobs.items()):
                if job["status"] not in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
                    continue

                # Parse the timestamp
                try:
                    updated_at = datetime.datetime.fromisoformat(job["updated_at"])
                    if now - updated_at > max_age:
                        jobs_to_remove.append(job_id)
                except (ValueError, KeyError):
                    # Skip jobs with invalid timestamps
                    continue

            # Remove the jobs
            for job_id in jobs_to_remove:
                job = self.jobs[job_id]
                status = job["status"]

                del self.jobs[job_id]

                if status == JobStatus.COMPLETED and job_id in self.completed_jobs:
                    del self.completed_jobs[job_id]
                elif status == JobStatus.FAILED and job_id in self.failed_jobs:
                    del self.failed_jobs[job_id]

                count += 1

            # Save changes if any jobs were removed
            if count > 0:
                self._save_jobs()

            return count
