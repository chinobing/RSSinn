from fastapi import APIRouter
from models.utils import fetch
from models.upptime import add_upptime_status
from fastapi_rss import RSSFeed, RSSResponse, Item
from faker import Faker
from datetime import datetime
from asyncache import cached
from cachetools import TTLCache
import json

yyets = APIRouter()

top_description=f"""
- 作者： [@chinobing](https://github.com/chinobing/)

- 来源：`https://yyets.dmesg.app/search`
- 参数：没有
- 状态： {add_upptime_status('yyets-top')}
"""

@yyets.get("/top/",
              summary="YYeTs-全站热搜",
              description=top_description)
@cached(TTLCache(1024, 300)) #cache result for 300 seconds
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
        title = json_item['name']
        img = json_item['posterLink']
        description = F"<img src='{img}'><br>{json_item['introduction']}<br>豆瓣：<a href=‘{json_item['doubanLink']}’>{title}</a>"
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



