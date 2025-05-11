"""
Steganography analysis API endpoints
"""

from flask import Blueprint, request, current_app, send_file
import os
import sys
import tempfile

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from engine.stegnox_engine import StegnoxEngine
from storage.storage_service import StorageService
from ...auth.auth import token_required
from ...utils.response import success_response, error_response
from ...utils.file_utils import save_uploaded_file
from ...utils.cache import cached
from ...utils.rate_limit import rate_limit

# Create blueprint
analysis_bp = Blueprint('analysis', __name__)

# Initialize services
engine = None
storage_service = None

@analysis_bp.before_request
def before_request():
    """Initialize services before each request"""
    global engine, storage_service
    if engine is None:
        engine = StegnoxEngine()
    if storage_service is None:
        storage_service = StorageService(storage_dir=current_app.config['STORAGE_DIR'])

@analysis_bp.route('/analyze', methods=['POST'])
@token_required
@rate_limit
def analyze_image(user_id, role):
    """Analyze an image for steganography"""
    # Check if file is in request
    if 'file' not in request.files:
        return error_response('No file part', 400)

    file = request.files['file']
    if file.filename == '':
        return error_response('No selected file', 400)

    # Save file
    filepath = save_uploaded_file(file)
    if not filepath:
        return error_response('Invalid file', 400)

    # Get methods from request
    methods = request.form.get('methods', 'all')

    try:
        # Analyze image
        if methods == 'all':
            results = engine.extract_all_methods(filepath)
        else:
            # Parse methods
            method_list = methods.split(',')
            results = {}

            for method_name in method_list:
                method_name = method_name.strip()
                method = getattr(engine, method_name, None)

                if method and callable(method):
                    results[method_name] = method(filepath)
                else:
                    results[method_name] = {'error': f'Method {method_name} not found'}

        # Save results
        storage_service.save_results(None, results)

        # Save image to storage
        storage_service.save_image(filepath)

        return success_response(results, 'Analysis completed successfully')

    except Exception as e:
        return error_response(f'Analysis failed: {str(e)}', 500)

@analysis_bp.route('/encode', methods=['POST'])
@token_required
@rate_limit
def encode_message(user_id, role):
    """Encode a message in an image"""
    # Check if file is in request
    if 'file' not in request.files:
        return error_response('No file part', 400)

    file = request.files['file']
    if file.filename == '':
        return error_response('No selected file', 400)

    # Get message and method from request
    message = request.form.get('message')
    method = request.form.get('method', 'lsb_encoding')

    if not message:
        return error_response('No message provided', 400)

    # Save input file
    input_filepath = save_uploaded_file(file)
    if not input_filepath:
        return error_response('Invalid file', 400)

    # Create temporary output file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        output_filepath = temp_file.name

    try:
        # Get encoding method
        encoding_method = getattr(engine, method, None)

        if not encoding_method or not callable(encoding_method):
            return error_response(f'Method {method} not found', 400)

        # Encode message
        result = encoding_method(input_filepath, message, output_filepath)

        if not result.get('success', False):
            return error_response(result.get('error', 'Encoding failed'), 500)

        # Save output image to storage
        stored_path = storage_service.save_image(output_filepath)

        # Get filename from stored path
        filename = os.path.basename(stored_path)

        return success_response({
            'message': result.get('message'),
            'filename': filename
        }, 'Message encoded successfully')

    except Exception as e:
        return error_response(f'Encoding failed: {str(e)}', 500)
    finally:
        # Clean up temporary file
        if os.path.exists(output_filepath):
            os.unlink(output_filepath)

@analysis_bp.route('/images/<filename>', methods=['GET'])
@token_required
@rate_limit
@cached(timeout=3600)  # Cache images for 1 hour
def get_image(filename, user_id, role):
    """Get an image from storage"""
    # Get image data
    image_data = storage_service.get_image(filename)

    if not image_data:
        return error_response('Image not found', 404)

    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(image_data)
        temp_filepath = temp_file.name

    try:
        # Determine content type based on file extension
        content_type = 'image/png'  # Default
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
            content_type = 'image/jpeg'
        elif filename.lower().endswith('.gif'):
            content_type = 'image/gif'
        elif filename.lower().endswith('.bmp'):
            content_type = 'image/bmp'

        # Send file
        return send_file(
            temp_filepath,
            mimetype=content_type,
            as_attachment=False,
            download_name=filename
        )

    except Exception as e:
        return error_response(f'Failed to retrieve image: {str(e)}', 500)
    finally:
        # Schedule file for deletion (will be deleted after response is sent)
        @analysis_bp.after_request
        def remove_file(response):
            if os.path.exists(temp_filepath):
                os.unlink(temp_filepath)
            return response
