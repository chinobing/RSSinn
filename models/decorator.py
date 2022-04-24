import hashlib
from typing import Optional
from starlette.requests import Request
from starlette.responses import Response
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi_cache.coder import PickleCoder
from models.read_yaml import parsing_yaml

cached_settings = parsing_yaml()['related_settings']['cached']
expiration_time = cached_settings['expiration_time']

def custom_key_builder(
        func,
        namespace: Optional[str] = "",
        request: Optional[Request] = None,
        response: Optional[Response] = None,
        args: Optional[tuple] = None,
        kwargs: Optional[dict] = None,
):
    """
    replace headers and _settings with empty string
    make cache remain unchanged even with headers and _settings params
    """
    prefix = f"{FastAPICache.get_prefix()}:{namespace}:"
    kwargs.update(headers="", _settings="")
    cache_key = (
            prefix
            + hashlib.md5(  # nosec:B303
        f"{func.__module__}:{func.__name__}:{args}:{kwargs}".encode()
        # f"{func.__module__}:{func.__name__}:{args}".encode()
    ).hexdigest()
    )
    return cache_key


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
    cache expires in three day
    """
    if fetch_cache_enabled == True:
        _cache = cache(namespace="fetch_content_cached", expire=259200, coder=PickleCoder, key_builder=custom_key_builder)
    else:
        _cache = nocache()
    return _cache
