"""
StegnoX Job Status Checker

This script demonstrates how to check the status of jobs in the queue.
"""

import os
import sys
import argparse
import json

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from steg_queue.job_queue import JobQueue, JobStatus
from storage.storage_service import StorageService

def main():
    parser = argparse.ArgumentParser(description="StegnoX Job Status Checker")
    parser.add_argument("--job-id", help="Job ID to check (if not specified, list all jobs)")
    parser.add_argument("--status", choices=["pending", "processing", "completed", "failed", "cancelled"],
                        help="Filter jobs by status")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of jobs to list")
    parser.add_argument("--offset", type=int, default=0, help="Offset for pagination")
    parser.add_argument("--storage-dir", default="data", help="Storage directory")
    parser.add_argument("--show-results", action="store_true", help="Show job results")
    args = parser.parse_args()
    
    # Initialize services
    storage = StorageService(storage_dir=os.path.join(args.storage_dir, "storage"))
    queue = JobQueue(storage_dir=os.path.join(args.storage_dir, "queue"))
    
    # Check specific job
    if args.job_id:
        job = queue.get_job(args.job_id)
        if not job:
            print(f"Error: Job {args.job_id} not found")
            return
        
        print(f"Job ID: {job['job_id']}")
        print(f"Status: {job['status'].value}")
        print(f"Priority: {job['priority'].value}")
        print(f"Image Path: {job['image_path']}")
        print(f"Created At: {job['created_at']}")
        print(f"Updated At: {job['updated_at']}")
        
        if "started_at" in job:
            print(f"Started At: {job['started_at']}")
        
        if "completed_at" in job:
            print(f"Completed At: {job['completed_at']}")
        
        if "failed_at" in job:
            print(f"Failed At: {job['failed_at']}")
        
        if "worker_id" in job:
            print(f"Worker ID: {job['worker_id']}")
        
        if "error" in job:
            print(f"Error: {job['error']}")
        
        if args.show_results and "results" in job:
            print("\nResults:")
            print(json.dumps(job["results"], indent=2))
        
        # If job is completed, also check storage for results
        if job["status"] == JobStatus.COMPLETED and args.show_results:
            storage_results = storage.get_results(args.job_id)
            if storage_results and "results" in storage_results:
                print("\nDetailed Results from Storage:")
                print(json.dumps(storage_results["results"], indent=2))
    
    # List jobs
    else:
        # Map status string to enum
        status = None
        if args.status:
            status_map = {
                "pending": JobStatus.PENDING,
                "processing": JobStatus.PROCESSING,
                "completed": JobStatus.COMPLETED,
                "failed": JobStatus.FAILED,
                "cancelled": JobStatus.CANCELLED
            }
            status = status_map[args.status]
        
        # Get jobs
        jobs = queue.list_jobs(status=status, limit=args.limit, offset=args.offset)
        
        if not jobs:
            print("No jobs found")
            return
        
        print(f"Found {len(jobs)} jobs:")
        for job in jobs:
            print(f"Job ID: {job['job_id']}, Status: {job['status'].value}, "
                  f"Priority: {job['priority'].value}, Created: {job['created_at']}")
        
        # Print queue stats
        stats = queue.get_queue_stats()
        print("\nQueue Stats:")
        print(f"Total Jobs: {stats['total_jobs']}")
        print(f"Pending: {stats['pending']['total']}")
        print(f"Processing: {stats['processing']}")
        print(f"Completed: {stats['completed']}")
        print(f"Failed: {stats['failed']}")

if __name__ == "__main__":
    main()
