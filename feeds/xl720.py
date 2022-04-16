from fastapi import APIRouter
from typing import Optional
from models.utils import fetch
from fastapi_rss import RSSFeed, RSSResponse, Item
from faker import Faker
from datetime import datetime

xl720 = APIRouter()

description=f"""
- 作者： [@chinobing](https://github.com/chinobing/)

- 来源：`https://www.xl720.com/`
- 参数： **id**
- 路由： `/xl720/?id=[]`
- Tips： 如：https://www.xl720.com/thunder/46198.html， `对应id为46198`
"""


@xl720.get("/",
              summary="迅雷电影天堂 xl720.com",
              description=description)
async def xl_movies(id:Optional[int] = None):
    fake = Faker()
    FAKE_HEADERS = {'User-Agent':fake.user_agent()}

    if id:
        url = f'https://www.xl720.com/thunder/{id}.html'
        post = await fetch(url, headers=FAKE_HEADERS)

        page_title = post.xpath("//h1[@class='postli-1']//text()").get()
        description = post.xpath("//div[@id='link-report']//text()").get()
        img =post.xpath("//div[@id='mainpic']/img/@src").get()
        episodes = post.xpath("//div[@id='zdownload']/div[@class='download-link']")
        items_list = []
        for ep in episodes:
            link = ep.xpath("./a/@href").get()
            title = ep.xpath("./a/text()").get().split('.')[0]
            des = f'<img src="{img}"><br>{description}<br> 磁力下载地址：<a href="{link}">{title}</a>'
            _item = Item(title=title, link=link, pub_date=datetime.now(), description=des)
            items_list.append(_item)

        feed_data = {
            'title': page_title,
            'link': url,
            'description': "迅雷电影天堂——最新高清迅雷电影电视剧下载网站",
            'item': items_list,
        }
        feed = RSSFeed(**feed_data)
        return RSSResponse(feed)


    url = 'https://www.xl720.com/new'

    tree = await fetch(url, headers=FAKE_HEADERS)
    posts = tree.xpath("//div[contains(@class,'post')]")

    items_list = []
    for post in posts:
        link = post.xpath(".//h3[contains(@class,'entry-title')]/a/@href").get()
        _title = post.xpath(".//h3[contains(@class,'entry-title')]//text()").get()
        _rating = post.xpath(".//div[contains(@class,'entry-rating')]//text()").get().replace(" ", "")
        title =f'[{_rating}]{_title}'
        description = post.xpath(".//div[contains(@class,'entry-excerpt')]/p/text()").get()
        _item = Item(title=title, link=link, pub_date=datetime.now(), description=description)
        items_list.append(_item)

    feed_data = {
        'title': '迅雷电影天堂 xl720.com',
        'link': 'https://www.xl720.com/',
        'description': "迅雷电影天堂——最新高清迅雷电影电视剧下载网站",
        'item': items_list,
    }
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)
