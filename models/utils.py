import asyncio
import json
import logging
from fastapi import Query, HTTPException
from parsel import Selector
from typing import Optional, Union, List, Tuple
from collections import Coroutine
from models.singletonAiohttp import SingletonAiohttp
from models.process_killer import checkIfProcessRunning, zombies_process_killer
from models.browser import Browser
from models.read_yaml import parsing_yaml
from models.decorator import fetch_content_cached

fetch_proxy_settings = parsing_yaml()['fetch_proxy_settings']
simple_proxy_settings = fetch_proxy_settings['simple']

DEFAULT_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

class filter_keywords:
    """preset params for filtering items from result.
    """
    def __init__(self,
                 include_keywords: Optional[str] = Query(None, description="**包括指定的关键字**，如`a-b-c-d, 则包括a、b、c、d四个关键字`"),
                 exclude_keywords: Optional[str] = Query(None, description="**不包括指定的关键字**，如`a-b-c-d， 则不包括a、b、c、d四个关键字`"),
                 ):
        """
        Construct a new 'filter_keywords' object.

        :param name: include_keywords, exclude_keywords
        :return: returns include_keywords, exclude_keywords
        """
        self.include_keywords = include_keywords
        self.exclude_keywords = exclude_keywords

async def fetch(urls: Union[str, List],
                headers: dict=DEFAULT_HEADERS,
                proxy: Optional[dict] = None,
                fetch_js:Optional[bool]=None,
                cache_enabled=False):
    """
    :param urls: str
    :param headers:dict
    :param proxy: {"proxy_server":"", "proxy_username":"", "proxy_password":""}
    :param fetch_js: True or False
    :param cache_enabled:  True or False
    :return: json or text with Selector
    """

    #proxy setup
    if isinstance(proxy, dict):
        if "proxy_server" in proxy:
            simple_proxy_settings.update(proxy_server=proxy['proxy_server'])
        if "proxy_username" in proxy:
            simple_proxy_settings.update(proxy_username=proxy['proxy_username'])
        if "proxy_password" in proxy:
            simple_proxy_settings.update(proxy_password=proxy['proxy_password'])

    # chrome zombies_process_killer
    if checkIfProcessRunning('chrome'):
        print('Yes a chrome process was running')
        await zombies_process_killer()

    # cache setup for fetch
    @fetch_content_cached(cache_enabled)
    async def query_url(urls, headers, _settings):
        ret = await SingletonAiohttp.query_url(urls, headers, _settings)
        if "ERROR" in ret or ret is None:
            return "ERROR"
            # raise HTTPException(status=500)
        return ret

    # fetch
    if isinstance(urls, str):
        if fetch_js == True:
            logger = logging.getLogger('browser')
            browser = Browser(simple_proxy_settings)
            await browser.start(headless=True)
            logger.info("Browser launched.")

            page = await browser.new_page()
            response = await page.goto(urls)
            if response.status != 200:
                await page.close()
                await browser.shutdown()
                raise HTTPException(status_code=404, detail="Item not found")
            res = await response.text()
            await page.close()
            await browser.shutdown()
            logger.info("Browser shutdown.")
        else:
            # res = await SingletonAiohttp.query_url(urls, headers=headers, _settings=fetch_proxy_settings)
            res = await query_url(urls, headers=headers, _settings=simple_proxy_settings)
            await SingletonAiohttp.close_aiohttp_client()

        if 'ERROR' in res:
            raise HTTPException(status_code=404, detail="Item not found")

        if fetch_js == True or validateJSON(res):
            return res

        tree = Selector(text=res)
        return tree

    if isinstance(urls, list):
        async_calls: List[Coroutine] = list()  # store all async operations
        for url in urls:
            if fetch_js == True:
                raise HTTPException(status_code=404, detail="fetch_js does not support multiple urls yet. ")
            else:
                # async_calls.append(SingletonAiohttp.query_url(url, headers=headers,  _settings=fetch_proxy_settings))
                async_calls.append(query_url(url, headers=headers, _settings=simple_proxy_settings))
                await SingletonAiohttp.close_aiohttp_client()

        all_results: List[Tuple] = await asyncio.gather(*async_calls)  # wait for all async operations

        if fetch_js == True or validateJSON(all_results[0]):
            trees = [res for res in all_results if "ERROR" not in res]
            if not trees:
                raise HTTPException(status_code=404, detail="Item not found")

            return trees

        trees = [Selector(text=res) for res in all_results if "ERROR" not in res]
        if not trees:
            raise HTTPException(status_code=404, detail="Item not found")
        return trees


def filter_content(item, filters: Optional[dict] = None):
    """
    :param items:
    :param filters: filters=Depends(filter_keywords)
    :return:  a mapping of member item->item.
    This maps all items from a list with customized include_keywords or exclude_keywords.
    Raw data will be returned if filters is not available.
    """
    if not filters.include_keywords and not filters.exclude_keywords:
        return True

    item_content = ''.join(str(x) for x in item)

    if filters.include_keywords:
        include_keywords = filters.include_keywords
        if '-' in include_keywords:
            in_kws = [inkw.strip() for inkw in include_keywords.split('-')]
        else:
            in_kws = [include_keywords]
        if any(x in item_content for x in in_kws):
            return True

    if filters.exclude_keywords:
        exclude_keywords = filters.exclude_keywords
        if '-' in exclude_keywords:
            ex_kws = [exkw.strip() for exkw in exclude_keywords.split('-')]
        else:
            ex_kws = [exclude_keywords]
        if not any(x in item_content for x in ex_kws):
            return True

    return False


def validateJSON(jsonData):
    """
    :param jsonData: json
    :return: True or False
    """
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True
