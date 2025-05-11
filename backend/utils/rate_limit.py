"""
Rate limiting middleware for StegnoX backend
"""

import time
import threading
from flask import request, jsonify, current_app
from functools import wraps

class RateLimiter:
    """Rate limiter implementation"""
    
    def __init__(self, limit=100, window=3600, by_ip=True, by_user=True):
        """
        Initialize the rate limiter
        
        Args:
            limit (int): Maximum number of requests allowed in the window
            window (int): Time window in seconds
            by_ip (bool): Whether to limit by IP address
            by_user (bool): Whether to limit by user ID
        """
        self.limit = limit
        self.window = window
        self.by_ip = by_ip
        self.by_user = by_user
        self.ip_counters = {}
        self.user_counters = {}
        self.lock = threading.RLock()
        
        # Start cleanup thread
        self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.cleanup_thread.start()
    
    def _get_key(self, request):
        """
        Get the key for rate limiting
        
        Args:
            request: Flask request object
            
        Returns:
            tuple: (ip_key, user_key)
        """
        ip_key = None
        user_key = None
        
        if self.by_ip:
            # Get client IP
            ip_key = request.remote_addr
            
            # Check for X-Forwarded-For header
            forwarded_for = request.headers.get('X-Forwarded-For')
            if forwarded_for:
                ip_key = forwarded_for.split(',')[0].strip()
        
        if self.by_user:
            # Get user ID from JWT token
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                try:
                    from ..auth.auth import decode_token
                    payload = decode_token(token)
                    if payload:
                        user_key = payload.get('sub')
                except ImportError:
                    pass
        
        return (ip_key, user_key)
    
    def is_allowed(self, request):
        """
        Check if the request is allowed
        
        Args:
            request: Flask request object
            
        Returns:
            bool: True if allowed, False if rate limited
        """
        with self.lock:
            ip_key, user_key = self._get_key(request)
            current_time = time.time()
            
            # Check IP rate limit
            if ip_key and self.by_ip:
                if ip_key not in self.ip_counters:
                    self.ip_counters[ip_key] = {'count': 0, 'reset_at': current_time + self.window}
                
                counter = self.ip_counters[ip_key]
                
                # Reset counter if window has passed
                if current_time > counter['reset_at']:
                    counter['count'] = 0
                    counter['reset_at'] = current_time + self.window
                
                # Check if limit exceeded
                if counter['count'] >= self.limit:
                    return False
                
                # Increment counter
                counter['count'] += 1
            
            # Check user rate limit
            if user_key and self.by_user:
                if user_key not in self.user_counters:
                    self.user_counters[user_key] = {'count': 0, 'reset_at': current_time + self.window}
                
                counter = self.user_counters[user_key]
                
                # Reset counter if window has passed
                if current_time > counter['reset_at']:
                    counter['count'] = 0
                    counter['reset_at'] = current_time + self.window
                
                # Check if limit exceeded
                if counter['count'] >= self.limit:
                    return False
                
                # Increment counter
                counter['count'] += 1
            
            return True
    
    def get_retry_after(self, request):
        """
        Get the retry-after time in seconds
        
        Args:
            request: Flask request object
            
        Returns:
            int: Seconds until rate limit resets
        """
        with self.lock:
            ip_key, user_key = self._get_key(request)
            current_time = time.time()
            retry_after = 0
            
            if ip_key and self.by_ip and ip_key in self.ip_counters:
                ip_reset_at = self.ip_counters[ip_key]['reset_at']
                ip_retry_after = max(0, int(ip_reset_at - current_time))
                retry_after = max(retry_after, ip_retry_after)
            
            if user_key and self.by_user and user_key in self.user_counters:
                user_reset_at = self.user_counters[user_key]['reset_at']
                user_retry_after = max(0, int(user_reset_at - current_time))
                retry_after = max(retry_after, user_retry_after)
            
            return retry_after
    
    def _cleanup_loop(self):
        """Cleanup expired counters periodically"""
        while True:
            time.sleep(60)  # Run cleanup every minute
            self._cleanup()
    
    def _cleanup(self):
        """Remove expired counters"""
        with self.lock:
            current_time = time.time()
            
            # Clean up IP counters
            for ip_key in list(self.ip_counters.keys()):
                if current_time > self.ip_counters[ip_key]['reset_at']:
                    del self.ip_counters[ip_key]
            
            # Clean up user counters
            for user_key in list(self.user_counters.keys()):
                if current_time > self.user_counters[user_key]['reset_at']:
                    del self.user_counters[user_key]

# Global rate limiter instance
rate_limiter = None

def get_rate_limiter():
    """
    Get or create the global rate limiter instance
    
    Returns:
        RateLimiter: Rate limiter instance
    """
    global rate_limiter
    if rate_limiter is None:
        # Get configuration from app config
        limit = current_app.config.get('RATE_LIMIT', 100)
        window = current_app.config.get('RATE_LIMIT_WINDOW', 3600)
        by_ip = current_app.config.get('RATE_LIMIT_BY_IP', True)
        by_user = current_app.config.get('RATE_LIMIT_BY_USER', True)
        
        rate_limiter = RateLimiter(limit=limit, window=window, by_ip=by_ip, by_user=by_user)
    
    return rate_limiter

def rate_limit(f):
    """
    Decorator for routes that should be rate limited
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        limiter = get_rate_limiter()
        
        if not limiter.is_allowed(request):
            retry_after = limiter.get_retry_after(request)
            
            response = jsonify({
                'success': False,
                'message': 'Rate limit exceeded',
                'error': {
                    'code': 'RATE_LIMIT_EXCEEDED',
                    'details': f'Try again in {retry_after} seconds'
                }
            })
            
            response.status_code = 429
            response.headers['Retry-After'] = str(retry_after)
            
            return response
        
        return f(*args, **kwargs)
    
    return decorated
