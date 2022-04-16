from fastapi import APIRouter
from models.utils import fetch
from fastapi_rss import RSSFeed, RSSResponse, Item
from faker import Faker
from datetime import datetime
from models.decorator import cached
import json
import re

chinastarmarket = APIRouter()

description=f"""
- 作者： [@chinobing](https://github.com/chinobing/)

- 来源：`https://www.chinastarmarket.cn/telegraph`
- 参数：没有
"""

@chinastarmarket.get("/telegraph/",
              summary="科创板电报",
              description=description)
@cached()
async def telegraph():
    url = 'https://www.chinastarmarket.cn/telegraph'

    fake = Faker()
    FAKE_HEADERS = {'User-Agent':fake.user_agent()}
    response = await fetch(url, headers=FAKE_HEADERS, fetch_js=True)
    data_text = re.findall(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', response)
    str_data = "".join(data_text)
    json_data = json.loads(str_data)
    item_list = json_data['props']['initialState']['telegraph']['telegraphList']

    items_list = []
    for item in item_list:
        title = item['title']
        description = item['content']
        link = 'https://www.chinastarmarket.cn/detail/'+ str(item['id'])
        ctime = item['ctime']
        pub_date = datetime.fromtimestamp(ctime)

        _item = Item(title=title, link=link, description=description, pub_date=pub_date)
        items_list.append(_item)

    feed_data = {
        'title': '科创板电报',
        'link': url,
        'description': "",
        'item': items_list,
    }
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)



