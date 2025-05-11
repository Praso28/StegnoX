"""
Performance monitoring utilities for StegnoX backend
"""

import time
import functools
import threading
import logging
import json
import os
from datetime import datetime
from flask import request, g, current_app

class PerformanceMonitor:
    """Performance monitoring for the application"""
    
    def __init__(self, app=None):
        """
        Initialize the performance monitor
        
        Args:
            app (Flask, optional): Flask application
        """
        self.app = app
        self.logger = logging.getLogger('stegnox.performance')
        self.metrics = {}
        self.lock = threading.RLock()
        
        # Initialize default settings
        self.enabled = True
        self.log_slow_requests = True
        self.slow_request_threshold = 1.0  # seconds
        self.metrics_file = None
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """
        Initialize the monitor with a Flask application
        
        Args:
            app (Flask): Flask application
        """
        self.app = app
        
        # Get configuration from app
        self.enabled = app.config.get('PERFORMANCE_MONITORING_ENABLED', True)
        self.log_slow_requests = app.config.get('LOG_SLOW_REQUESTS', True)
        self.slow_request_threshold = app.config.get('SLOW_REQUEST_THRESHOLD', 1.0)
        
        # Set up metrics file
        metrics_dir = app.config.get('METRICS_DIR', os.path.join(app.config['STORAGE_DIR'], 'metrics'))
        os.makedirs(metrics_dir, exist_ok=True)
        self.metrics_file = os.path.join(metrics_dir, 'performance_metrics.json')
        
        # Load existing metrics
        self._load_metrics()
        
        # Set up request handlers
        app.before_request(self._before_request)
        app.after_request(self._after_request)
        
        # Set up periodic metrics saving
        self._start_metrics_saver()
        
        self.logger.info("Performance monitoring initialized")
    
    def _before_request(self):
        """Before request handler"""
        if not self.enabled:
            return
        
        g.start_time = time.time()
    
    def _after_request(self, response):
        """
        After request handler
        
        Args:
            response: Flask response
            
        Returns:
            response: Flask response
        """
        if not self.enabled or not hasattr(g, 'start_time'):
            return response
        
        # Calculate request duration
        duration = time.time() - g.start_time
        
        # Log slow requests
        if self.log_slow_requests and duration > self.slow_request_threshold:
            self.logger.warning(f"Slow request: {request.method} {request.path} took {duration:.2f}s")
        
        # Record metrics
        self._record_request_metric(request.path, request.method, duration, response.status_code)
        
        return response
    
    def _record_request_metric(self, path, method, duration, status_code):
        """
        Record a request metric
        
        Args:
            path (str): Request path
            method (str): HTTP method
            duration (float): Request duration in seconds
            status_code (int): HTTP status code
        """
        with self.lock:
            # Initialize metrics for this path if not exists
            if path not in self.metrics:
                self.metrics[path] = {
                    'count': 0,
                    'total_time': 0,
                    'avg_time': 0,
                    'min_time': float('inf'),
                    'max_time': 0,
                    'methods': {},
                    'status_codes': {},
                    'last_request': None
                }
            
            # Update path metrics
            self.metrics[path]['count'] += 1
            self.metrics[path]['total_time'] += duration
            self.metrics[path]['avg_time'] = self.metrics[path]['total_time'] / self.metrics[path]['count']
            self.metrics[path]['min_time'] = min(self.metrics[path]['min_time'], duration)
            self.metrics[path]['max_time'] = max(self.metrics[path]['max_time'], duration)
            self.metrics[path]['last_request'] = datetime.now().isoformat()
            
            # Update method metrics
            if method not in self.metrics[path]['methods']:
                self.metrics[path]['methods'][method] = 0
            self.metrics[path]['methods'][method] += 1
            
            # Update status code metrics
            status_key = str(status_code)
            if status_key not in self.metrics[path]['status_codes']:
                self.metrics[path]['status_codes'][status_key] = 0
            self.metrics[path]['status_codes'][status_key] += 1
    
    def _load_metrics(self):
        """Load metrics from file"""
        if not self.metrics_file or not os.path.exists(self.metrics_file):
            return
        
        try:
            with open(self.metrics_file, 'r') as f:
                self.metrics = json.load(f)
            self.logger.info(f"Loaded performance metrics from {self.metrics_file}")
        except Exception as e:
            self.logger.error(f"Error loading metrics: {str(e)}")
    
    def _save_metrics(self):
        """Save metrics to file"""
        if not self.metrics_file:
            return
        
        try:
            with self.lock:
                with open(self.metrics_file, 'w') as f:
                    json.dump(self.metrics, f, indent=2)
            self.logger.info(f"Saved performance metrics to {self.metrics_file}")
        except Exception as e:
            self.logger.error(f"Error saving metrics: {str(e)}")
    
    def _start_metrics_saver(self):
        """Start a thread to periodically save metrics"""
        def saver_thread():
            while True:
                time.sleep(300)  # Save every 5 minutes
                self._save_metrics()
        
        thread = threading.Thread(target=saver_thread, daemon=True)
        thread.start()
    
    def get_metrics(self):
        """
        Get all metrics
        
        Returns:
            dict: Performance metrics
        """
        with self.lock:
            return self.metrics.copy()
    
    def get_path_metrics(self, path):
        """
        Get metrics for a specific path
        
        Args:
            path (str): Request path
            
        Returns:
            dict: Path metrics or None if not found
        """
        with self.lock:
            return self.metrics.get(path)
    
    def reset_metrics(self):
        """Reset all metrics"""
        with self.lock:
            self.metrics = {}
            self._save_metrics()

# Create a global monitor instance
performance_monitor = PerformanceMonitor()

def measure_performance(func):
    """
    Decorator to measure function performance
    
    Args:
        func: Function to measure
        
    Returns:
        function: Decorated function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not performance_monitor.enabled:
            return func(*args, **kwargs)
        
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        
        # Log slow functions
        if duration > performance_monitor.slow_request_threshold:
            performance_monitor.logger.warning(f"Slow function: {func.__module__}.{func.__name__} took {duration:.2f}s")
        
        return result
    
    return wrapper
