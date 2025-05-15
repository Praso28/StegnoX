# StegnoX Job Queue System

The Job Queue System is responsible for managing and processing steganography analysis jobs in the StegnoX application. It provides a thread-safe, persistent queue with priority support.

## Features

- **Priority Queuing**: Support for high, normal, and low priority jobs
- **Job Status Tracking**: Track job status through its lifecycle (pending, processing, completed, failed, cancelled)
- **Persistence**: Jobs are automatically saved to disk and can be restored after restart
- **Thread Safety**: All operations are thread-safe for use in multi-threaded environments
- **Job Management**: Comprehensive API for adding, retrieving, and managing jobs
- **Statistics**: Get detailed statistics about the queue state
- **Cleanup**: Automatically clean up old completed jobs

## Usage

### Basic Usage

```python
from steg_queue.job_queue import JobQueue, JobStatus, JobPriority

# Create a job queue
queue = JobQueue(storage_dir="queue_data")

# Add a job
job_id = queue.add_job("path/to/image.png", priority=JobPriority.HIGH)

# Get the next job to process
job = queue.get_next_job()
if job:
    # Process the job
    try:
        # Do processing...
        results = {"found_data": True, "message": "Secret message found"}
        queue.mark_job_complete(job["job_id"], results)
    except Exception as e:
        queue.mark_job_failed(job["job_id"], str(e))

# Get job information
job_info = queue.get_job(job_id)

# List jobs
pending_jobs = queue.list_jobs(status=JobStatus.PENDING)

# Get queue statistics
stats = queue.get_queue_stats()
```

### Worker Implementation

Here's an example of how to implement a worker process:

```python
import time
from steg_queue.job_queue import JobQueue
from engine.stegnox_engine import StegnoxEngine

def worker_process(worker_id):
    queue = JobQueue()
    engine = StegnoxEngine()
    
    while True:
        # Get the next job
        job = queue.get_next_job(worker_id=worker_id)
        
        if job:
            try:
                # Process the job
                image_path = job["image_path"]
                results = engine.extract_all_methods(image_path)
                
                # Mark as complete
                queue.mark_job_complete(job["job_id"], results)
                print(f"Worker {worker_id}: Completed job {job['job_id']}")
            except Exception as e:
                # Mark as failed
                queue.mark_job_failed(job["job_id"], str(e))
                print(f"Worker {worker_id}: Failed job {job['job_id']}: {str(e)}")
        else:
            # No jobs available, wait before checking again
            time.sleep(1)
```

## API Reference

### Job Management

- `add_job(image_path, job_id=None, priority=JobPriority.NORMAL, metadata=None)`: Add a new job to the queue
- `get_next_job(worker_id=None)`: Get the next job from the queue
- `mark_job_complete(job_id, results=None)`: Mark a job as complete with results
- `mark_job_failed(job_id, error=None)`: Mark a job as failed
- `cancel_job(job_id)`: Cancel a pending job
- `get_job(job_id)`: Get job information
- `list_jobs(status=None, limit=10, offset=0)`: List jobs with optional filtering

### Queue Management

- `get_queue_stats()`: Get statistics about the job queue
- `cleanup_old_jobs(max_age_days=30)`: Remove old completed and failed jobs

## Development

### Testing

Run the tests to ensure the job queue is working correctly:

```bash
python -m unittest tests/test_queue.py
```

### Adding New Features

When adding new features to the job queue:

1. Add the new method to the `JobQueue` class
2. Ensure thread safety with the `lock`
3. Update the persistence mechanism if needed
4. Add tests for the new functionality
5. Update this documentation
