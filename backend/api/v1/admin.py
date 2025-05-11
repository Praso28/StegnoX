"""
Admin API endpoints
"""

from flask import Blueprint, request, current_app
import os
import sys

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from ...auth.auth import admin_required
from ...utils.response import success_response, error_response
from ...utils.performance import performance_monitor
from ...utils.cache import cache
from ...utils.rate_limit import rate_limit

# Create blueprint
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/metrics', methods=['GET'])
@admin_required
def get_metrics(user_id, role):
    """Get performance metrics"""
    try:
        metrics = performance_monitor.get_metrics()
        return success_response(metrics, 'Performance metrics retrieved successfully')
    except Exception as e:
        return error_response(f'Failed to retrieve metrics: {str(e)}', 500)

@admin_bp.route('/metrics/reset', methods=['POST'])
@admin_required
def reset_metrics(user_id, role):
    """Reset performance metrics"""
    try:
        performance_monitor.reset_metrics()
        return success_response(None, 'Performance metrics reset successfully')
    except Exception as e:
        return error_response(f'Failed to reset metrics: {str(e)}', 500)

@admin_bp.route('/cache/clear', methods=['POST'])
@admin_required
def clear_cache(user_id, role):
    """Clear the cache"""
    try:
        cache.clear()
        return success_response(None, 'Cache cleared successfully')
    except Exception as e:
        return error_response(f'Failed to clear cache: {str(e)}', 500)

@admin_bp.route('/system/info', methods=['GET'])
@admin_required
def system_info(user_id, role):
    """Get system information"""
    try:
        import platform
        import psutil
        
        # Get system info
        system_data = {
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'cpu_count': psutil.cpu_count(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory': {
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available,
                'percent': psutil.virtual_memory().percent
            },
            'disk': {
                'total': psutil.disk_usage('/').total,
                'used': psutil.disk_usage('/').used,
                'free': psutil.disk_usage('/').free,
                'percent': psutil.disk_usage('/').percent
            }
        }
        
        return success_response(system_data, 'System information retrieved successfully')
    except ImportError:
        # psutil might not be installed
        return error_response('System monitoring libraries not available', 500)
    except Exception as e:
        return error_response(f'Failed to retrieve system info: {str(e)}', 500)
