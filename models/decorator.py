from asyncache import cached
from cachetools import TTLCache
from models.read_yaml import parsing_yaml

cached_settings = parsing_yaml()['related_settings']['cached']
expiration_time = cached_settings['expiration_time']
maxsize = cached_settings['maxsize']


def nocache(*args, **kwargs):
    def decorator(func):
        return func
    return decorator

def cache():
    if cached_settings['enabled'] == False:
        _cache = nocache
    else:
        _cache = cached(TTLCache(maxsize=maxsize,  ttl=expiration_time))

    return _cache
