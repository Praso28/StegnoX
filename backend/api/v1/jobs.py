"""
Job management API endpoints
"""

from flask import Blueprint, request, current_app
import os
import sys

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from steg_queue.job_queue import JobQueue, JobPriority, JobStatus
from storage.storage_service import StorageService
from ...auth.auth import token_required
from ...utils.response import success_response, error_response
from ...utils.file_utils import save_uploaded_file

# Create blueprint
jobs_bp = Blueprint('jobs', __name__)

# Initialize services
job_queue = None
storage_service = None

@jobs_bp.before_request
def before_request():
    """Initialize services before each request"""
    global job_queue, storage_service
    if job_queue is None:
        job_queue = JobQueue(storage_dir=current_app.config['QUEUE_DIR'])
    if storage_service is None:
        storage_service = StorageService(storage_dir=current_app.config['STORAGE_DIR'])

@jobs_bp.route('', methods=['POST'])
@token_required
def create_job(user_id, role):
    """Create a new job"""
    # Check if file is in request
    if 'file' not in request.files:
        return error_response('No file part', 400)
    
    file = request.files['file']
    if file.filename == '':
        return error_response('No selected file', 400)
    
    # Get priority from request
    priority_str = request.form.get('priority', 'normal').lower()
    priority_map = {
        'low': JobPriority.LOW,
        'normal': JobPriority.NORMAL,
        'high': JobPriority.HIGH
    }
    priority = priority_map.get(priority_str, JobPriority.NORMAL)
    
    # Save file
    filepath = save_uploaded_file(file)
    if not filepath:
        return error_response('Invalid file', 400)
    
    # Create metadata
    metadata = {
        'user_id': user_id,
        'original_filename': file.filename
    }
    
    # Add job to queue
    job_id = job_queue.add_job(filepath, priority=priority, metadata=metadata)
    
    # Return job information
    job = job_queue.get_job(job_id)
    
    return success_response({
        'job_id': job_id,
        'status': job['status'].value,
        'created_at': job['created_at']
    }, 'Job created successfully', 201)

@jobs_bp.route('', methods=['GET'])
@token_required
def list_jobs(user_id, role):
    """List jobs"""
    # Get query parameters
    status_str = request.args.get('status')
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    
    # Convert status string to enum
    status = None
    if status_str:
        status_map = {
            'pending': JobStatus.PENDING,
            'processing': JobStatus.PROCESSING,
            'completed': JobStatus.COMPLETED,
            'failed': JobStatus.FAILED,
            'cancelled': JobStatus.CANCELLED
        }
        status = status_map.get(status_str.lower())
    
    # Get jobs
    jobs = job_queue.list_jobs(status=status, limit=limit, offset=offset)
    
    # Filter jobs by user_id if not admin
    if role != 'admin':
        jobs = [job for job in jobs if job.get('metadata', {}).get('user_id') == user_id]
    
    # Format jobs for response
    formatted_jobs = []
    for job in jobs:
        formatted_job = {
            'job_id': job['job_id'],
            'status': job['status'].value,
            'priority': job['priority'].value,
            'created_at': job['created_at'],
            'updated_at': job['updated_at']
        }
        
        if 'started_at' in job:
            formatted_job['started_at'] = job['started_at']
        
        if 'completed_at' in job:
            formatted_job['completed_at'] = job['completed_at']
        
        if 'failed_at' in job:
            formatted_job['failed_at'] = job['failed_at']
        
        if 'metadata' in job:
            formatted_job['metadata'] = job['metadata']
        
        formatted_jobs.append(formatted_job)
    
    return success_response(formatted_jobs, 'Jobs retrieved successfully')

@jobs_bp.route('/<job_id>', methods=['GET'])
@token_required
def get_job(job_id, user_id, role):
    """Get job details"""
    # Get job
    job = job_queue.get_job(job_id)
    
    if not job:
        return error_response('Job not found', 404)
    
    # Check if user has access to this job
    if role != 'admin' and job.get('metadata', {}).get('user_id') != user_id:
        return error_response('Access denied', 403)
    
    # Format job for response
    formatted_job = {
        'job_id': job['job_id'],
        'status': job['status'].value,
        'priority': job['priority'].value,
        'created_at': job['created_at'],
        'updated_at': job['updated_at'],
        'image_path': job['image_path']
    }
    
    if 'started_at' in job:
        formatted_job['started_at'] = job['started_at']
    
    if 'completed_at' in job:
        formatted_job['completed_at'] = job['completed_at']
    
    if 'failed_at' in job:
        formatted_job['failed_at'] = job['failed_at']
    
    if 'metadata' in job:
        formatted_job['metadata'] = job['metadata']
    
    if 'worker_id' in job:
        formatted_job['worker_id'] = job['worker_id']
    
    if 'error' in job:
        formatted_job['error'] = job['error']
    
    # Get results if job is completed
    if job['status'] == JobStatus.COMPLETED:
        # Try to get results from job
        if 'results' in job:
            formatted_job['results'] = job['results']
        else:
            # Try to get results from storage
            results = storage_service.get_results(job_id)
            if results:
                formatted_job['results'] = results
    
    return success_response(formatted_job, 'Job retrieved successfully')

@jobs_bp.route('/<job_id>', methods=['DELETE'])
@token_required
def cancel_job(job_id, user_id, role):
    """Cancel a job"""
    # Get job
    job = job_queue.get_job(job_id)
    
    if not job:
        return error_response('Job not found', 404)
    
    # Check if user has access to this job
    if role != 'admin' and job.get('metadata', {}).get('user_id') != user_id:
        return error_response('Access denied', 403)
    
    # Check if job can be cancelled
    if job['status'] != JobStatus.PENDING:
        return error_response('Only pending jobs can be cancelled', 400)
    
    # Cancel job
    success = job_queue.cancel_job(job_id)
    
    if not success:
        return error_response('Failed to cancel job', 500)
    
    return success_response(None, 'Job cancelled successfully')
