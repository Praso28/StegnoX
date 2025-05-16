"""
Analysis blueprint
"""

import os
from flask import Blueprint, request, jsonify, current_app, send_file
from werkzeug.utils import secure_filename
from ...utils.security import token_required
from ...engine.stegnox_engine import StegnoxEngine
import json

analysis_bp = Blueprint('analysis', __name__)

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@analysis_bp.route('/analyze', methods=['POST'])
@token_required
def analyze(current_user):
    """Analyze an image."""
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'message': 'No file part'
        }), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({
            'success': False,
            'message': 'No selected file'
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'message': 'File type not allowed'
        }), 400

    # Save file
    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Analyze image
    engine = StegnoxEngine()
    results = engine.analyze_image(filepath)

    # Save results
    results_filename = f'{os.path.splitext(filename)[0]}_results.json'
    results_filepath = os.path.join(current_app.config['RESULTS_FOLDER'], results_filename)
    with open(results_filepath, 'w') as f:
        json.dump(results, f)

    return jsonify({
        'success': True,
        'data': results
    })

@analysis_bp.route('/encode', methods=['POST'])
@token_required
def encode(current_user):
    """Encode a message in an image."""
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'message': 'No file part'
        }), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({
            'success': False,
            'message': 'No selected file'
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'message': 'File type not allowed'
        }), 400

    message = request.form.get('message')
    if not message:
        return jsonify({
            'success': False,
            'message': 'No message provided'
        }), 400

    method = request.form.get('method', 'lsb_encoding')

    # Save file
    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Encode message
    engine = StegnoxEngine()
    output_filepath = os.path.join(
        current_app.config['RESULTS_FOLDER'],
        f'encoded_{filename}'
    )
    success = engine.encode_message(filepath, output_filepath, message, method)

    if not success:
        return jsonify({
            'success': False,
            'message': 'Failed to encode message'
        }), 500

    return jsonify({
        'success': True,
        'data': {
            'filename': f'encoded_{filename}'
        }
    })

@analysis_bp.route('/download/<filename>')
@token_required
def download(current_user, filename):
    """Download a file."""
    filepath = os.path.join(current_app.config['RESULTS_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({
            'success': False,
            'message': 'File not found'
        }), 404

    return send_file(filepath, as_attachment=True)
