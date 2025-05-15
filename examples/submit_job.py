"""
StegnoX Job Submission Example

This script demonstrates how to submit jobs to the queue.
"""

import os
import sys
import argparse

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from steg_queue.job_queue import JobQueue, JobPriority
from storage.storage_service import StorageService

def main():
    parser = argparse.ArgumentParser(description="StegnoX Job Submission")
    parser.add_argument("--image", required=True, help="Path to the image file")
    parser.add_argument("--priority", choices=["low", "normal", "high"], default="normal",
                        help="Job priority")
    parser.add_argument("--storage-dir", default="data", help="Storage directory")
    parser.add_argument("--metadata", help="Additional metadata (key1=value1,key2=value2)")
    args = parser.parse_args()
    
    # Map priority string to enum
    priority_map = {
        "low": JobPriority.LOW,
        "normal": JobPriority.NORMAL,
        "high": JobPriority.HIGH
    }
    priority = priority_map[args.priority]
    
    # Parse metadata
    metadata = {}
    if args.metadata:
        for item in args.metadata.split(','):
            if '=' in item:
                key, value = item.split('=', 1)
                metadata[key.strip()] = value.strip()
    
    # Initialize services
    storage = StorageService(storage_dir=os.path.join(args.storage_dir, "storage"))
    queue = JobQueue(storage_dir=os.path.join(args.storage_dir, "queue"))
    
    # Save the image to storage
    print(f"Saving image: {args.image}")
    image_path = storage.save_image(args.image)
    if not image_path:
        print(f"Error: Failed to save image {args.image}")
        return
    
    # Add job to queue
    print(f"Submitting job with priority: {args.priority}")
    job_id = queue.add_job(image_path, priority=priority, metadata=metadata)
    
    print(f"Job submitted successfully!")
    print(f"Job ID: {job_id}")
    
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
