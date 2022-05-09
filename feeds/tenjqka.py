from fastapi import APIRouter
from models.utils import fetch
from fastapi_rss import RSSFeed, RSSResponse, Item
from faker import Faker
from datetime import datetime
from models.decorator import cached
import json

tenjqka = APIRouter()

"""
-------------------------------------------------
   Description :     同花顺财经-实时快讯
   Modified_date：   2022/04/19
-------------------------------------------------
"""
realtimenews_description=f"""
- 作者： [@chinobing](https://github.com/chinobing/)

- 来源：`https://news.10jqka.com.cn/realtimenews.html`
- 参数：没有
"""
@tenjqka.get("/realtimenews",
              summary="同花顺财经-实时快讯",
              description=realtimenews_description)
@cached()
async def realtimenews():
    url = 'https://news.10jqka.com.cn/tapp/news/push/stock/?page=1&tag=&track=website&pagesize=100'

    fake = Faker()
    FAKE_HEADERS = {'User-Agent':fake.user_agent()}

    str_data = await fetch(url, headers=FAKE_HEADERS)
    json_data = json.loads(str_data)
    data = json_data['data']

    items_list = []
    for item in data['list']:
        title = item['title']
        description = item['digest']
        link = item['url']
        ctime = int(item['ctime'])
        pub_date = datetime.fromtimestamp(ctime)

        _item = Item(title=title, link=link, description=description, pub_date=pub_date)
        items_list.append(_item)

    feed_data = {
        'title': '同花顺财经-实时快讯',
        'link': url,
        'description': "",
        'item': items_list,
    }
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)




