import logging
from typing import Optional
from playwright.async_api import async_playwright, Playwright, BrowserContext

logger = logging.getLogger('browser')

class Browser:

    def __init__(self, settings=None):
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[BrowserContext] = None
        self._settings = settings
        self.cookies = []

    async def start(self, *args, **kwargs):
        if not self._playwright:
            self._playwright = await async_playwright().start()
        if not self._browser:
            if self._settings and self._settings['proxy_server'] \
                    and self._settings['proxy_username'] and self._settings['proxy_password']:
                self._browser = await self._playwright.chromium.launch_persistent_context(
                    "browser_data/", java_script_enabled=True, args=["--disable-notifications"],
                    proxy={
                        "server": self._settings['proxy_server'],
                        "username": self._settings['proxy_username'],
                        "password": self._settings['proxy_password']},
                    **kwargs)
                logger.info(f"Browser launched with proxy {self._settings['proxy_server']}")
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
