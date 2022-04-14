# import asyncio
# from typing import Optional
# from playwright.async_api import async_playwright
#
#
#
# class SingletonPlaywright:
#     sem: asyncio.Semaphore = None
#     playwright_client: async_playwright() = None
#
#     @classmethod
#     async def get_playwright_client(cls) -> async_playwright:
#         if cls.playwright_client is None:
#             cls.playwright_client = await async_playwright().start()
#
#         return cls.playwright_client
#
#     @classmethod
#     async def close_requests_client(cls):
#         if cls.playwright_client:
#             await cls.playwright_client.stop()
#             cls.playwright_client = None
#
#     @classmethod
#     async def query_url(cls, url: str,
#                         headers: Optional[dict] = None,
#                         proxy: Optional[str] = None,
#                         ):
#         client = await cls.get_playwright_client()
#
#         try:
#             browser = await client.chromium.launch(proxy=proxy)
#             context = await browser.new_context()
#             page = await context.new_page()
#             await page.goto(url)
#             response = await page.content()
#             await cls.close_requests_client()
#
#         except Exception as e:
#             return {"ERROR": e}
#
#         return response
#


import logging
from typing import Optional

from playwright.async_api import async_playwright, Playwright, BrowserContext

# from facebook_rss import local_cookies
# from facebook_rss.utils.pickling import pickle_, unpickle
from settings import get_settings, Settings


logger = logging.getLogger('browser')


class Browser:

    def __init__(self, settings=None):
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[BrowserContext] = None
        self._settings: Settings = settings
        self.cookies = []

    async def start(self, *args, **kwargs):
        if not self._playwright:
            self._playwright = await async_playwright().start()
        if not self._browser:
            if self._settings and self._settings.PROXY_SERVER \
                    and self._settings.PROXY_USERNAME and self._settings.PROXY_PASSWORD:
                self._browser = await self._playwright.chromium.launch_persistent_context(
                    "browser_data/", java_script_enabled=True, args=["--disable-notifications"],
                    proxy={
                        "server": self._settings.PROXY_SERVER,
                        "username": self._settings.PROXY_USERNAME,
                        "password": self._settings.PROXY_PASSWORD},
                    **kwargs)
                logger.info(f"Browser launched with proxy {self._settings.PROXY_SERVER}")
            else:
                self._browser = await self._playwright.chromium.launch_persistent_context(
                    "browser_data/", java_script_enabled=True, args=["--disable-notifications"], **kwargs)

    async def new_page(self):
        return await self._browser.new_page()

    async def add_cookies(self, cookies):
        if cookies:
            await self._browser.add_cookies(cookies)

    async def shutdown(self):
        # await self._browser_context.close()
        await self._browser.close()
        await self._playwright.stop()

    async def get_cookies(self):
        self.cookies = await self._browser.cookies()
        return self.cookies


# Dependency
async def get_browser() -> Browser:
    browser = Browser(get_settings())
    await browser.start(headless=True)
    # await browser.add_cookies(unpickle(local_cookies))
    logger.info("Browser launched with saved cookies.")
    try:
        yield browser
    finally:
        if len(browser.cookies) > 2:
            # pickle_(browser.cookies)
            logger.info("Saved updated Browser cookies locally.")
        await browser.shutdown()
        logger.info("Browser shutdown.")