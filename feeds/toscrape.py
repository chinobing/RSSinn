from fastapi import APIRouter, Depends
from typing import Optional
from models.utils import DEFAULT_HEADERS, fetch, filter_keywords, filter_content
from fastapi_rss import RSSFeed, RSSResponse, Item
from faker import Faker
from models.decorator import cached

toscrape = APIRouter()

url = 'https://quotes.toscrape.com/'

"""
-------------------------------------------------
   Description :     Toscrape.com, 获取首页所有quotes
   Modified_date：   2022/04/19
-------------------------------------------------
"""
@toscrape.get("/quotes/",
              summary="获取首页所有quotes",
              description="直接输入网址获取首页所有quotes")
async def quotes():
    fake = Faker()
    FAKE_HEADERS = {'User-Agent':fake.user_agent()}
    tree = await fetch(url, headers=FAKE_HEADERS)
    posts = tree.xpath("//div[@class='quote']")

    items_list = []
    for post in posts:
        author = post.xpath(".//small[@class='author']//text()").get()
        description = post.xpath("./span[@class='text']//text()").get()
        _item = Item(title=author, author=author,description=description)
        items_list.append(_item)

    feed_data = {
        'title': 'Toscrape.com',
        'link': 'toscrape.com',
        'description': "",
        'item': items_list,
    }
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)

"""
-------------------------------------------------
   Description :     Toscrape.com, 获取带指定tag的所有quotes
   Modified_date：   2022/04/19
-------------------------------------------------
"""
@toscrape.get("/quotes_tag/",
              summary="获取带指定tag的所有quotes",
              description="输入指定的tag获取quotes")
async def quotes_tag(tag:Optional[str] = None):
    def parse(post):
        item = {}
        item['description'] = post.xpath("./span[@class='text']//text()").get()
        item['author'] = post.xpath(".//small[@class='author']//text()").get()
        return item

    if tag:
        link = f'{url}/tag/{tag}'
    else:
        link = url
    tree = await fetch(link, headers=DEFAULT_HEADERS)
    posts = tree.xpath("//div[@class='quote']")
    items = list(map(parse, posts))

    items_list = []
    for _item in items:
        item = Item(title=_item['author'], author=_item['author'], description=_item['description'])
        items_list.append(item)

    feed_data = {
        'title': 'toscrape with tag',
        'link': 'toscrape.com',
        'description': "",
        'item': items_list,
    }
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)

"""
-------------------------------------------------
   Description :     Toscrape.com, 获取带指定关键字的所有quotes
   Modified_date：   2022/04/19
-------------------------------------------------
"""
@toscrape.get("/quotes_with_filter/",
              summary="获取带指定关键字的所有quotes",
              description="`inculde_keywords`：包含指定的关键字；`exclude_keywords`：不含指定关键字；")
async def quotes_with_filter(filters=Depends(filter_keywords)):
    def parse(post):
        item = {}
        item['description'] = post.xpath("./span[@class='text']//text()").get()
        item['author'] = post.xpath(".//small[@class='author']//text()").get()
        return item

    tree = await fetch(url, headers=DEFAULT_HEADERS)
    posts = tree.xpath("//div[@class='quote']")
    items = list(map(parse, posts))
    items = filter_content(items,filters)

    items_list = []
    for _item in items:
        item = Item(title=_item['author'], author=_item['author'], description=_item['description'])
        items_list.append(item)

    feed_data = {
        'title': 'toscrape with content filter',
        'link': 'toscrape.com',
        'description': "",
        'item': items_list,
    }
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)

"""
-------------------------------------------------
   Description :     Toscrape.com, 获取作者介绍的数据，并使用了cache来缓存结果
   Modified_date：   2022/04/19
-------------------------------------------------
"""
@toscrape.get("/authors/", summary='关于作者介绍',
              description='获取次页面的数据，并使用了cache来缓存结果')
@cached()
async def authors():
    tree = await fetch(url)
    if not tree:
        return
    links = tree.xpath("//div[@class='quote']/span/a/@href").getall()
    links = [f'{url}{uri}' for uri in links]

    results = await fetch(links, headers=DEFAULT_HEADERS, cache_enabled=True)
    if not results:
        return

    items_list = []
    for link, each in zip(links, results):
        author = each.xpath("//h3[@class='author-title']//text()").get()
        description = each.xpath("//div[@class='author-description']//text()").get()
        _item = Item(title=author, link=link, author=author, description=description)
        items_list.append(_item)

    feed_data = {
        'title': 'author page',
        'link': 'toscrape.com',
        'description': "",
        'item': items_list,
    }
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)
