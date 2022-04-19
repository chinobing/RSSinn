# from asyncache import cached
# from cachetools import TTLCache
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
        _cache = cache(namespace="rssinn", expire=expiration_time, coder=PickleCoder)
    else:
        _cache = nocache()

        # _cache = cached(TTLCache(maxsize=maxsize,  ttl=expiration_time))
    return _cache
