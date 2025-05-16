"""
Job management API endpoints
"""

from flask import Blueprint, request, current_app, jsonify
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
    """Initialize job queue."""
    if not hasattr(current_app, 'job_queue'):
        current_app.job_queue = JobQueue(storage_dir=current_app.config['QUEUE_DIR'])

@jobs_bp.route('/', methods=['GET'])
@token_required
def list_jobs(current_user):
    """List all jobs."""
    jobs = current_app.job_queue.list_jobs()
    return jsonify({
        'success': True,
        'data': jobs
    })

@jobs_bp.route('/', methods=['POST'])
@token_required
def create_job(current_user):
    """Create a new job."""
    data = request.get_json()
    job_id = current_app.job_queue.add_job(
        job_type=data.get('type'),
        priority=data.get('priority', 1),
        parameters=data.get('parameters', {})
    )
    return jsonify({
        'success': True,
        'job_id': job_id
    })

@jobs_bp.route('/<job_id>', methods=['GET'])
@token_required
def get_job(current_user, job_id):
    """Get job details."""
    job = current_app.job_queue.get_job(job_id)
    if not job:
        return jsonify({
            'success': False,
            'message': 'Job not found'
        }), 404
    return jsonify({
        'success': True,
        'data': job
    })

@jobs_bp.route('/<job_id>', methods=['DELETE'])
@token_required
def cancel_job(current_user, job_id):
    """Cancel a job."""
    success = current_app.job_queue.cancel_job(job_id)
    if not success:
        return jsonify({
            'success': False,
            'message': 'Job not found'
        }), 404
    return jsonify({
        'success': True,
        'message': 'Job cancelled'
    })
