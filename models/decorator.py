# from asyncache import cached
# from cachetools import TTLCache
from typing import Optional
from fastapi_cache.decorator import cache
from fastapi_cache.coder import PickleCoder
from models.read_yaml import parsing_yaml

cached_settings = parsing_yaml()['related_settings']['cached']
expiration_time = cached_settings['expiration_time']

def nocache(*args, **kwargs):
    def decorator(func):
        return func
    return decorator

def cached(namespace: Optional[str]=None):
    if cached_settings['enabled'] == False:
        _cache = nocache(namespace=namespace)

    if cached_settings['enabled'] == True:
        if cached_settings['method']=="in-memory":
            _cache = cache(namespace=namespace, expire=expiration_time, coder=PickleCoder)
        if cached_settings['method']=="redis":
            _cache = cache(namespace=namespace, expire=expiration_time, coder=PickleCoder)

        # _cache = cached(TTLCache(maxsize=maxsize,  ttl=expiration_time))
    return _cache
