import asyncio
import requests_html
from typing import Optional


#fastAPI-aiohttp-example
#https://github.com/raphaelauv/fastAPI-aiohttp-example/blob/b5b55592807ed2f8218511a986c6519babc66d11/src/fastAPI_aiohttp/fastAPI.py
class SingletonRequestsHtml:
    sem: asyncio.Semaphore = None
    requests_client: requests_html.AsyncHTMLSession = None

    @classmethod
    def get_requests_client(cls) -> requests_html.AsyncHTMLSession:
        if cls.requests_client is None:
            cls.requests_client = requests_html.AsyncHTMLSession()

        return cls.requests_client

    @classmethod
    async def close_requests_client(cls):
        if cls.requests_client:
            await cls.requests_client.close()
            cls.requests_client = None

    @classmethod
    async def query_url(cls, url: str,
                        headers: Optional[dict] = None,
                        proxy: Optional[str] = None,
                        ):
        client = cls.get_requests_client()

        try:
            response = await client.get(url, headers=headers, proxies={'http':proxy})
            cls.close_requests_client()
            if response.status_code != 200:
                return {"ERROR OCCURED" + str(await response.html.arender())}
            await response.html.arender(timeout=20, sleep=2)

        except Exception as e:
            return {"ERROR": e}

        return response.text

