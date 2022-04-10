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
                        proxy: Optional[str] = None,
                        ):
        client = cls.get_aiohttp_client()

        try:
            async with client.get(url, headers=headers, proxy=proxy) as response:
                if response.status != 200:
                    # return {"ERROR OCCURED" + str(await response.text())}
                    cls.close_aiohttp_client()
                    raise HTTPException(status_code=response.status, detail="Item not found, please try again!")
                text_result = await response.text()
        except Exception as e:
            return {"ERROR": e}

        return text_result