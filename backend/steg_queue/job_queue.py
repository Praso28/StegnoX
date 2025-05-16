"""
Job queue implementation
"""

import os
import json
import time
from enum import Enum
from datetime import datetime

class JobStatus(Enum):
    """Job status enum."""
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'

class JobQueue:
    """Job queue implementation."""

    def __init__(self, storage_dir):
        """Initialize job queue."""
        self.storage_dir = storage_dir
        self.jobs_file = os.path.join(storage_dir, 'jobs.json')
        self._load_jobs()

    def _load_jobs(self):
        """Load jobs from storage."""
        if not os.path.exists(self.jobs_file):
            self.jobs = {}
            self._save_jobs()
        else:
            with open(self.jobs_file, 'r') as f:
                self.jobs = json.load(f)

    def _save_jobs(self):
        """Save jobs to storage."""
        os.makedirs(os.path.dirname(self.jobs_file), exist_ok=True)
        with open(self.jobs_file, 'w') as f:
            json.dump(self.jobs, f)

    def add_job(self, job_type, priority=1, parameters=None):
        """Add a new job to the queue."""
        job_id = str(int(time.time() * 1000))  # Use timestamp as job ID
        job = {
            'job_id': job_id,
            'type': job_type,
            'priority': priority,
            'parameters': parameters or {},
            'status': JobStatus.PENDING.value,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        self.jobs[job_id] = job
        self._save_jobs()
        return job_id

    def get_job(self, job_id):
        """Get job details."""
        return self.jobs.get(job_id)

    def list_jobs(self, status=None):
        """List all jobs."""
        jobs = list(self.jobs.values())
        if status:
            jobs = [job for job in jobs if job['status'] == status.value]
        return jobs

    def update_job(self, job_id, status, results=None, error=None):
        """Update job status."""
        if job_id not in self.jobs:
            return False

        job = self.jobs[job_id]
        job['status'] = status.value
        job['updated_at'] = datetime.now().isoformat()

        if status == JobStatus.COMPLETED and results is not None:
            job['results'] = results

        if status == JobStatus.FAILED and error is not None:
            job['error'] = error

        self._save_jobs()
        return True

    def cancel_job(self, job_id):
        """Cancel a job."""
        if job_id not in self.jobs:
            return False

        job = self.jobs[job_id]
        if job['status'] == JobStatus.PENDING.value:
            job['status'] = JobStatus.CANCELLED.value
            job['updated_at'] = datetime.now().isoformat()
            self._save_jobs()
            return True

        return False

    def cleanup_old_jobs(self, max_age_days=7):
        """Clean up old jobs."""
        now = datetime.now()
        old_jobs = []

        for job_id, job in self.jobs.items():
            created_at = datetime.fromisoformat(job['created_at'])
            age_days = (now - created_at).days

            if age_days > max_age_days:
                old_jobs.append(job_id)

        for job_id in old_jobs:
            del self.jobs[job_id]

        if old_jobs:
            self._save_jobs()

        return len(old_jobs) 