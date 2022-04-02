from fastapi import APIRouter
from models.utils import fetch
from models.upptime import add_upptime_status
from fastapi_rss import RSSFeed, RSSResponse, Item
from faker import Faker
from datetime import datetime
from asyncache import cached
from cachetools import TTLCache
import json
import re

kr = APIRouter()

description=f"""
- 作者： [@chinobing](https://github.com/chinobing/)

- 来源：`https://36kr.com/newsflashes/`
- 参数：没有
- 状态： {add_upptime_status('36kr')}
"""


@kr.get("/newsflashes/",
              summary="36kr-实时快讯",
              description=description)

@cached(TTLCache(1024, 300)) #cache result for 300 seconds
async def newsflashes():
    url = 'https://36kr.com/newsflashes/'

    fake = Faker()
    FAKE_HEADERS = {'User-Agent':fake.user_agent()}
    response = await fetch(url, headers=FAKE_HEADERS, fetch_js=True)
    data_text = re.findall(r'<script>window.initialState=(.*?)</', response)
    str_data = "".join(data_text)
    json_data = json.loads(str_data)
    item_list = json_data['newsflashCatalogData']['data']['newsflashList']['data']['itemList']

    items_list = []
    for item in item_list:
        title = item['templateMaterial']['widgetTitle']
        description = item['templateMaterial']['widgetContent']
        link = 'https://36kr.com/newsflashes/' + str(item['templateMaterial']['itemId'])
        ctime = int(item['templateMaterial']['publishTime']/1000.00)
        pub_date = datetime.fromtimestamp(ctime)

        _item = Item(title=title, link=link, description=description, pub_date=pub_date)
        items_list.append(_item)

    feed_data = {
        'title': '36kr-实时快讯',
        'link': url,
        'description': "",
        'item': items_list,
    }
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)




