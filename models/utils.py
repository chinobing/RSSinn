import asyncio
from fastapi import Query
from parsel import Selector
from typing import Optional, Union, List, Tuple
from requests_html import AsyncHTMLSession
from models.process_killer import zombies_process_killer

from collections import Coroutine
from pages.index import SingletonAiohttp


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

# async def fetch(url: str,
#                 headers: dict=DEFAULT_HEADERS,
#                 proxies: Optional[Union[str, dict]] = None,
#                 fetch_js:Optional[bool]=None):
#     if fetch_js == True:
#         try:
#             asession = AsyncHTMLSession()
#             r = await asession.get(url, headers=headers, proxies=proxies)
#             await r.html.arender(timeout=20, sleep=2)
#             await asession.close()
#         except Exception as e:
#             print(f'[Err] {e}')
#             zombies_process_killer()
#         else:
#             return r.text
#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url, headers=headers, proxy=proxies) as resp:
#                 res = await resp.text()
#                 tree = Selector(text=res)
#                 return tree
#     except Exception as e:
#         print(f'[Err] {e}')



async def fetch(urls: Union[str, List],
                headers: dict=DEFAULT_HEADERS,
                proxy: Optional[str] = None,
                fetch_js:Optional[bool]=None):
    if fetch_js == True:
        try:
            asession = AsyncHTMLSession()
            r = await asession.get(urls, headers=headers, proxies={'http': proxy})
            await r.html.arender(timeout=20, sleep=2)
            await asession.close()
        except Exception as e:
            print(f'[Err] {e}')
            zombies_process_killer()
        else:
            return r.text

    if isinstance(urls, str):
        res = await SingletonAiohttp.query_url(urls, headers=headers, proxy=proxy)
        if 'ERROR' in res:
            return ""
        tree = Selector(text=res)
        return tree

    if isinstance(urls, list):
        async_calls: List[Coroutine] = list()  # store all async operations
        for url in urls:
            async_calls.append(SingletonAiohttp.query_url(url, headers=headers, proxy=proxy))

        all_results: List[Tuple] = await asyncio.gather(*async_calls)  # wait for all async operations
        if 'ERROR' in all_results:
            return ""
        trees = [Selector(text=res) for res in all_results if "ERROR" not in res]
        return trees

        return all_results




def filter_content(items, filters: Optional[dict] = None):
    """Returns a mapping of member item->item.
    This maps all items from a list with customized include_keywords or exclude_keywords.
    Raw data will be returned if filters is not available.
    """
    if not filters.include_keywords and not filters.exclude_keywords:
        return items

    content = []
    for item in items:
        item_content = ''.join(str(x) for x in item.values())

        if filters.include_keywords:
            include_keywords = filters.include_keywords
            if '-' in include_keywords:
                in_kws = [inkw.strip() for inkw in include_keywords.split('-')]
            else:
                in_kws = [include_keywords]
            if any(x in item_content for x in in_kws):
                content.append(item)

        if filters.exclude_keywords:
            exclude_keywords = filters.exclude_keywords
            if '-' in exclude_keywords:
                ex_kws = [exkw.strip() for exkw in exclude_keywords.split('-')]
            else:
                ex_kws = [exclude_keywords]
            if not any(x in item_content for x in ex_kws):
                content.append(item)

    return [dict(t) for t in {tuple(d.items()) for d in content}]

