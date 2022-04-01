import aiohttp
from fastapi import Query
from parsel import Selector
from typing import Optional, Union
from requests_html import AsyncHTMLSession


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

##################################################################################
from functools import partial, wraps
def hash_dict(func):
    """Transform mutable dictionnary
    Into immutable
    Useful to be compatible with cache
    """
    class HDict(dict):
        def __hash__(self):
            return hash(frozenset(self.items()))

    @wraps(func)
    def wrapped(*args, **kwargs):
        args = tuple([HDict(arg) if isinstance(arg, dict) else arg for arg in args])
        kwargs = {k: HDict(v) if isinstance(v, dict) else v for k, v in kwargs.items()}
        return func(*args, **kwargs)
    return wrapped

async def fetch(url: str,
                headers: dict=DEFAULT_HEADERS,
                proxies: Optional[Union[str, dict]] = None,
                fetch_js:Optional[bool]=None):
    if fetch_js == True:
        asession = AsyncHTMLSession()
        r = await asession.get(url, headers=headers, proxies=proxies)
        await r.html.arender()
        await asession.close()
        return r.text

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, proxy=proxies) as resp:
            res = await resp.text()
            tree = Selector(text=res)
            return tree

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

