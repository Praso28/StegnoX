# StegnoX Examples

This directory contains example scripts demonstrating how to use the StegnoX components.

## Engine Demo

The `engine_demo.py` script demonstrates how to use the StegnoX engine for steganography analysis and encoding.

```bash
# Analyze an image with all methods
python examples/engine_demo.py --action analyze --image path/to/image.png

# Encode a message using LSB steganography
python examples/engine_demo.py --action encode --method lsb --image path/to/cover.png --message "Secret message" --output path/to/output.png

# Decode a message from an image
python examples/engine_demo.py --action decode --method lsb --image path/to/stego_image.png
```

## Job Queue System

The following scripts demonstrate how to use the job queue system:

### Submit Job

The `submit_job.py` script shows how to submit a job to the queue:

```bash
# Submit a job with normal priority
python examples/submit_job.py --image path/to/image.png

# Submit a job with high priority
python examples/submit_job.py --image path/to/image.png --priority high

# Submit a job with metadata
python examples/submit_job.py --image path/to/image.png --metadata "source=upload,user=john"
```

### Check Job Status

The `check_job.py` script shows how to check the status of jobs:

```bash
# Check a specific job
python examples/check_job.py --job-id job_123

# Check a specific job and show results
python examples/check_job.py --job-id job_123 --show-results

# List all jobs
python examples/check_job.py

# List completed jobs
python examples/check_job.py --status completed

# List jobs with pagination
python examples/check_job.py --limit 5 --offset 10
```

### Worker Process

The `worker.py` script demonstrates how to implement a worker process that processes jobs from the queue:

```bash
# Start a worker
python examples/worker.py

# Start a worker with a custom ID
python examples/worker.py --worker-id worker_1

# Start a worker with a custom storage directory
python examples/worker.py --storage-dir /path/to/data
```

## Complete Workflow Example

Here's an example of a complete workflow:

1. Start a worker in one terminal:
   ```bash
   python examples/worker.py
   ```

2. Submit a job in another terminal:
   ```bash
   python examples/submit_job.py --image path/to/image.png --priority high
   ```

3. Check the job status:
   ```bash
   python examples/check_job.py --job-id <job_id_from_step_2> --show-results
   ```

The worker will automatically process the job, and you can check the results using the check_job script.
