import asyncio
from typing import Optional
from playwright.async_api import async_playwright



class SingletonPlaywright:
    sem: asyncio.Semaphore = None
    playwright_client: async_playwright() = None

    @classmethod
    async def get_playwright_client(cls) -> async_playwright:
        if cls.playwright_client is None:
            cls.playwright_client = await async_playwright().start()

        return cls.playwright_client

    @classmethod
    async def close_requests_client(cls):
        if cls.playwright_client:
            await cls.playwright_client.stop()
            cls.playwright_client = None

    @classmethod
    async def query_url(cls, url: str,
                        headers: Optional[dict] = None,
                        proxy: Optional[str] = None,
                        ):
        client = await cls.get_playwright_client()

        try:
            browser = await client.chromium.launch(proxy=proxy)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url)
            response = await page.content()
            await cls.close_requests_client()

        except Exception as e:
            return {"ERROR": e}

        return response

