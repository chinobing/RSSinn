from fastapi_cache.decorator import cache
from fastapi_cache.coder import PickleCoder
from models.read_yaml import parsing_yaml

cached_settings = parsing_yaml()['related_settings']['cached']
expiration_time = cached_settings['expiration_time']

def nocache(*args, **kwargs):
    def decorator(func):
        return func
    return decorator

def cached():
    if cached_settings['enabled'] == True:
        _cache = cache(namespace="feeds", expire=expiration_time, coder=PickleCoder)
    else:
        _cache = nocache()
    return _cache

def fetch_content_cached(fetch_cache_enabled):
    """
    cache webpage content by url
    cache expires in one day
    """
    if fetch_cache_enabled == True:
        _cache = cache(namespace="fetch_content_cached", expire=86400, coder=PickleCoder)
    else:
        _cache = nocache()
    return _cache
