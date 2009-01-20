import settings  # When using Django so as to skip the cache during testing.
import logging
from google.appengine.api import memcache

def memoize(key, time=60):
    """Decorator to memoize functions using memcache."""
    def decorator(fxn):
        def wrapper(*args, **kwargs):
            data = memcache.get(key)
            if data is not None:
                logging.error("returning cache data for key %s", key)
                return data
            data = fxn(*args, **kwargs)
            logging.error("caching to key %s", key)
            memcache.set(key, data, time)
            return data
        return wrapper
    return decorator #if not settings.DEBUG else fxn

def memoize_params(keyformat, time=60):
    """Decorator to memoize_params functions using memcache. Requires that you have one %s pr parameter to the function"""
    def decorator(fxn):
        def wrapper(*args, **kwargs):
            key = keyformat % args[0:keyformat.count('%')]
            data = memcache.get(key)
            if data is not None:
                logging.error("returning cache data for key %s", key)
                return data
            data = fxn(*args, **kwargs)
            logging.error("caching to key %s", key)
            memcache.set(key, data, time)
            return data
        return wrapper
    return decorator #if not settings.DEBUG else fxn