"""
StegnoX Worker Example

This script demonstrates how to implement a worker process that processes jobs from the queue.
"""

import os
import sys
import time
import uuid
import argparse
import threading
import signal
import datetime

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from queue.job_queue import JobQueue, JobStatus, JobPriority
from engine.stegnox_engine import StegnoxEngine
from storage.storage_service import StorageService

class Worker:
    def __init__(self, worker_id=None, storage_dir="data"):
        """
        Initialize a worker
        
        Args:
            worker_id (str, optional): Worker ID. If None, a UUID will be generated.
            storage_dir (str): Directory for storage
        """
        self.worker_id = worker_id or f"worker_{uuid.uuid4()}"
        self.queue = JobQueue(storage_dir=os.path.join(storage_dir, "queue"))
        self.engine = StegnoxEngine()
        self.storage = StorageService(storage_dir=os.path.join(storage_dir, "storage"))
        self.running = False
        self.thread = None
        
        # Statistics
        self.stats = {
            "jobs_processed": 0,
            "jobs_completed": 0,
            "jobs_failed": 0,
            "start_time": None,
            "last_job_time": None
        }
    
    def start(self):
        """Start the worker thread"""
        if self.running:
            print(f"Worker {self.worker_id} is already running")
            return
        
        self.running = True
        self.stats["start_time"] = datetime.datetime.now()
        self.thread = threading.Thread(target=self._worker_loop)
        self.thread.daemon = True
        self.thread.start()
        print(f"Worker {self.worker_id} started")
    
    def stop(self):
        """Stop the worker thread"""
        if not self.running:
            print(f"Worker {self.worker_id} is not running")
            return
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print(f"Worker {self.worker_id} stopped")
    
    def _worker_loop(self):
        """Main worker loop"""
        while self.running:
            try:
                # Get the next job
                job = self.queue.get_next_job(worker_id=self.worker_id)
                
                if job:
                    self.stats["jobs_processed"] += 1
                    self.stats["last_job_time"] = datetime.datetime.now()
                    
                    try:
                        # Process the job
                        print(f"Worker {self.worker_id}: Processing job {job['job_id']}")
                        image_path = job["image_path"]
                        
                        # Run all extraction methods
                        results = self.engine.extract_all_methods(image_path)
                        
                        # Save results to storage
                        self.storage.save_results(job["job_id"], results)
                        
                        # Mark job as complete
                        self.queue.mark_job_complete(job["job_id"], results)
                        self.stats["jobs_completed"] += 1
                        print(f"Worker {self.worker_id}: Completed job {job['job_id']}")
                    
                    except Exception as e:
                        # Mark job as failed
                        self.queue.mark_job_failed(job["job_id"], str(e))
                        self.stats["jobs_failed"] += 1
                        print(f"Worker {self.worker_id}: Failed job {job['job_id']}: {str(e)}")
                
                else:
                    # No jobs available, wait before checking again
                    time.sleep(1)
            
            except Exception as e:
                print(f"Worker {self.worker_id}: Error in worker loop: {str(e)}")
                time.sleep(5)  # Wait a bit longer after an error
    
    def get_stats(self):
        """Get worker statistics"""
        stats = self.stats.copy()
        
        # Calculate uptime
        if stats["start_time"]:
            uptime = datetime.datetime.now() - stats["start_time"]
            stats["uptime_seconds"] = uptime.total_seconds()
            stats["uptime_str"] = str(uptime).split('.')[0]  # Remove microseconds
        
        # Add queue stats
        stats["queue"] = self.queue.get_queue_stats()
        
        return stats

def main():
    parser = argparse.ArgumentParser(description="StegnoX Worker")
    parser.add_argument("--worker-id", help="Worker ID")
    parser.add_argument("--storage-dir", default="data", help="Storage directory")
    args = parser.parse_args()
    
    # Create worker
    worker = Worker(worker_id=args.worker_id, storage_dir=args.storage_dir)
    
    # Handle signals for graceful shutdown
    def signal_handler(sig, frame):
        print("Shutting down worker...")
        worker.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start worker
    worker.start()
    
    # Print stats periodically
    try:
        while True:
            time.sleep(10)
            stats = worker.get_stats()
            print(f"\nWorker {worker.worker_id} Stats:")
            print(f"Uptime: {stats.get('uptime_str', 'N/A')}")
            print(f"Jobs Processed: {stats['jobs_processed']}")
            print(f"Jobs Completed: {stats['jobs_completed']}")
            print(f"Jobs Failed: {stats['jobs_failed']}")
            print(f"Queue Stats: {stats['queue']['pending']['total']} pending, "
                  f"{stats['queue']['processing']} processing, "
                  f"{stats['queue']['completed']} completed, "
                  f"{stats['queue']['failed']} failed")
    except KeyboardInterrupt:
        worker.stop()

if __name__ == "__main__":
    main()
