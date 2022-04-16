from fastapi import APIRouter
from models.utils import fetch
from fastapi_rss import RSSFeed, RSSResponse, Item
from faker import Faker
from datetime import datetime
from models.decorator import cached
import json
import re

yyets = APIRouter()


"""
yyets 全站热搜  
"""
top_description=f"""
- 作者： [@chinobing](https://github.com/chinobing/)

- 来源：`https://yyets.dmesg.app/search`
- 参数：没有
"""

@yyets.get("/top/",
              summary="YYeTs-全站热搜",
              description=top_description)
@cached("yyets-top")
async def top():
    url = 'https://yyets.dmesg.app/api/top'

    fake = Faker()
    FAKE_HEADERS = {'User-Agent':fake.user_agent()}

    str_data = await fetch(url, headers=FAKE_HEADERS)
    json_data = json.loads(str_data)
    data_all = json_data['ALL']
    links = [f"https://yyets.dmesg.app/api/douban?resource_id={x['data']['info']['id']}" for x in data_all]
    results = await fetch(links)
    if not results:
        return

    items_list = []
    for item in results:
        json_item = json.loads(item)
        _rating = f"[{json_item['rating']}]分" if "rating" in json_item else ""
        title = f"{_rating}{json_item['name']}"
        img = json_item['posterLink']
        description = f"<img src='{img}'><br>{json_item['introduction']}<br><br>豆瓣地址：<a href=‘{json_item['doubanLink']}’>{title}</a>"
        link = f"https://yyets.dmesg.app/resource?id={json_item['resourceId']}"
        releaseDate = json_item['releaseDate'][:10]
        pub_date = datetime.strptime(releaseDate, '%Y-%m-%d')

        _item = Item(title=title, link=link, description=description, pub_date=pub_date)
        items_list.append(_item)

    feed_data = {
        'title': 'YYeTs-全站热搜',
        'link': url,
        'description': "",
        'item': items_list,
    }
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)


"""
yyets 评论区资源-阿里云盘
"""
discuss_description=f"""
- 作者： [@chinobing](https://github.com/chinobing/)

- 来源：`https://yyets.dmesg.app/discuss`
- 参数：没有
"""

@yyets.get("/discuss/",
              summary="YYeTs-评论区资源-阿里云盘",
              description=discuss_description)
@cached("yyets-discuss")
async def discuss():
    url = 'https://yyets.dmesg.app/api/comment?resource_id=233&page=1&size=20'

    fake = Faker()
    FAKE_HEADERS = {'User-Agent':fake.user_agent()}

    str_data = await fetch(url, headers=FAKE_HEADERS)
    json_data = json.loads(str_data)
    results = json_data['data']

    if not results:
        return

    items_list = []
    for item in results:
        content = item['content']
        if 'http' in content and 'aliyundrive' in content:
            title = content.split('http')[0]
            description = content
            link = re.search(r"https://www.aliyundrive.com/s/(.*?)...........", content).group()
            pub_date = datetime.strptime(item['date'], '%Y-%m-%d %H:%M:%S')

            _item = Item(title=title, link=link, description=description, pub_date=pub_date)
            items_list.append(_item)

    feed_data = {
        'title': 'YYeTs-评论区资源-阿里云盘',
        'link': url,
        'description': "",
        'item': items_list,
    }
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)
