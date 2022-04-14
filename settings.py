from fastapi import FastAPI

# https://python.land/data-processing/python-yaml

#设置upptime status的路径， https://upptime.js.org/， 地址为https://cdn.jsdelivr.net/gh/github账户/repo名称@master
upptime_status_url = 'https://cdn.jsdelivr.net/gh/chinobing/upptime-rssinn@master'





#设置网站的基本信息
def app_settings() -> FastAPI():
    return {
        'title': 'RSS inn - RSS小黑屋',
        'description': 'Powered by FastAPI',
        'swagger_ui_parameters': {
                                "defaultModelsExpandDepth": -1,
                                "filter": True
                                  },
            }


from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Facebook to RSS API"
    USE_KEY: bool = False  # Use secret key for API requests. Enable this if you want and edit API_KEY below.
    API_KEY: str = "abcdefghijklmnopqrstuvwxyz0123456789"
    # Playwright Browser Connection
    PROXY_SERVER: str = ""  # Supports http and socks proxies.
    PROXY_USERNAME: str = ""
    PROXY_PASSWORD: str = ""
    # Facebook related settings
    LANGUAGE_CODE: str = "en"  # Supports EN only currently.
    SITE: str = "mbasic"
    USE_ACCOUNT: bool = True
    # RSS settings
    EXPIRATION_TIME: int = 30  # Time in minutes for cached feeds to expire after


@lru_cache()
def get_settings():
    return Settings()