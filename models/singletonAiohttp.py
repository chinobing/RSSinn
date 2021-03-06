import asyncio
import aiohttp
from socket import AF_INET
from typing import Optional
from fastapi import HTTPException

SIZE_POOL_AIOHTTP = 100

#fastAPI-aiohttp-example
#https://github.com/raphaelauv/fastAPI-aiohttp-example/blob/b5b55592807ed2f8218511a986c6519babc66d11/src/fastAPI_aiohttp/fastAPI.py
class SingletonAiohttp:
    sem: asyncio.Semaphore = None
    aiohttp_client: aiohttp.ClientSession = None

    @classmethod
    def get_aiohttp_client(cls) -> aiohttp.ClientSession:
        if cls.aiohttp_client is None:
            timeout = aiohttp.ClientTimeout(total=20)
            connector = aiohttp.TCPConnector(family=AF_INET, limit_per_host=SIZE_POOL_AIOHTTP, enable_cleanup_closed=True)
            cls.aiohttp_client = aiohttp.ClientSession(timeout=timeout, connector=connector)

        return cls.aiohttp_client

    @classmethod
    async def close_aiohttp_client(cls):
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    @classmethod
    async def query_url(cls, url: str,
                        headers: Optional[dict] = None,
                        _settings: Optional[dict] = None,
                        ):
        client = cls.get_aiohttp_client()

        if _settings["proxy_username"]:
            proxy_auth = aiohttp.BasicAuth(_settings['proxy_username'], _settings['proxy_password'])
        else:
            proxy_auth = None
        if _settings["proxy_server"]:
            proxy_server = _settings['proxy_server']
        else:
            proxy_server = None
        try:
            async with client.get(url, headers=headers, proxy=proxy_server, proxy_auth=proxy_auth) as response:
                if response.status != 200:
                    cls.close_aiohttp_client()
                    raise HTTPException(status_code=response.status, detail="Item not found, please try again!")
                text_result = await response.text()
        except Exception as e:
            return "ERROR"
        return text_result