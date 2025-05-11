"""
Caching utilities for StegnoX backend
"""

import json
import hashlib
import functools
import time
from flask import current_app, request

# Try to import Redis, but make it optional
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

class Cache:
    """Redis-based cache implementation"""
    
    def __init__(self, app=None):
        """
        Initialize the cache
        
        Args:
            app (Flask, optional): Flask application
        """
        self.app = app
        self.redis = None
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """
        Initialize the cache with a Flask application
        
        Args:
            app (Flask): Flask application
        """
        self.app = app
        
        # Check if Redis is available
        if not REDIS_AVAILABLE:
            app.logger.warning("Redis not available. Caching disabled.")
            return
        
        # Get Redis configuration from app config
        redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/0')
        
        try:
            self.redis = redis.from_url(redis_url)
            app.logger.info(f"Cache initialized with Redis at {redis_url}")
        except redis.exceptions.ConnectionError:
            app.logger.warning(f"Could not connect to Redis at {redis_url}. Caching disabled.")
            self.redis = None
    
    def _generate_key(self, key_prefix, args, kwargs):
        """
        Generate a cache key
        
        Args:
            key_prefix (str): Prefix for the key
            args: Function arguments
            kwargs: Function keyword arguments
            
        Returns:
            str: Cache key
        """
        # Create a string representation of the arguments
        arg_string = str(args) + str(sorted(kwargs.items()))
        
        # Hash the arguments
        arg_hash = hashlib.md5(arg_string.encode()).hexdigest()
        
        # Combine prefix and hash
        return f"{key_prefix}:{arg_hash}"
    
    def get(self, key):
        """
        Get a value from the cache
        
        Args:
            key (str): Cache key
            
        Returns:
            object: Cached value or None if not found
        """
        if not self.redis:
            return None
        
        try:
            value = self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            self.app.logger.error(f"Cache get error: {str(e)}")
            return None
    
    def set(self, key, value, timeout=None):
        """
        Set a value in the cache
        
        Args:
            key (str): Cache key
            value (object): Value to cache
            timeout (int, optional): Cache timeout in seconds
        """
        if not self.redis:
            return
        
        try:
            self.redis.set(key, json.dumps(value), ex=timeout)
        except Exception as e:
            self.app.logger.error(f"Cache set error: {str(e)}")
    
    def delete(self, key):
        """
        Delete a value from the cache
        
        Args:
            key (str): Cache key
        """
        if not self.redis:
            return
        
        try:
            self.redis.delete(key)
        except Exception as e:
            self.app.logger.error(f"Cache delete error: {str(e)}")
    
    def clear(self):
        """Clear all cached values"""
        if not self.redis:
            return
        
        try:
            self.redis.flushdb()
        except Exception as e:
            self.app.logger.error(f"Cache clear error: {str(e)}")

# Create a global cache instance
cache = Cache()

def cached(timeout=300, key_prefix=None):
    """
    Decorator for caching function results
    
    Args:
        timeout (int): Cache timeout in seconds
        key_prefix (str, optional): Prefix for cache keys
        
    Returns:
        function: Decorated function
    """
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            # Skip cache in debug mode if configured
            if current_app.config.get('CACHE_DISABLED_IN_DEBUG', False) and current_app.debug:
                return f(*args, **kwargs)
            
            # Generate cache key
            prefix = key_prefix or f.__module__ + '.' + f.__name__
            cache_key = cache._generate_key(prefix, args, kwargs)
            
            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Call the function and cache the result
            start_time = time.time()
            result = f(*args, **kwargs)
            duration = time.time() - start_time
            
            # Only cache if execution took longer than threshold
            min_duration = current_app.config.get('CACHE_MIN_DURATION', 0.1)
            if duration >= min_duration:
                cache.set(cache_key, result, timeout)
            
            return result
        return decorated_function
    return decorator
