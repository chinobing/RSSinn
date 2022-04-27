from fastapi import APIRouter, Depends
from models.utils import fetch, filter_keywords, filter_content
from fastapi_rss import RSSFeed, RSSResponse, Item
from faker import Faker
from datetime import datetime
from models.decorator import cached
import json

kr = APIRouter()

"""
-------------------------------------------------
   Description :     36kr-实时快讯
   Modified at ：     2022/04/19
-------------------------------------------------
"""
description=f"""
- 作者： [@chinobing](https://github.com/chinobing/)

- 来源：`https://36kr.com/newsflashes/`
- 参数：没有
"""
@kr.get("/newsflashes/",
              summary="36kr-实时快讯",
              description=description)
@cached()
async def newsflashes():
    url = 'https://36kr.com/newsflashes/'

    fake = Faker()
    FAKE_HEADERS = {'Host':'36kr.com', 'User-Agent':fake.user_agent()}
    response = await fetch(url, headers=FAKE_HEADERS)
    data_text = response.re(r'<script>window.initialState=(.*?)</')[0]
    str_data = "".join(data_text)
    json_data = json.loads(str_data)
    if json_data['newsflashCatalogData']:
        item_list = json_data['newsflashCatalogData']['data']['newsflashList']['data']['itemList']
    else:
        item_list = json_data['newsflashList']['flow']['itemList']

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


"""
-------------------------------------------------
   Description :     36kr-实时快讯
   Modified at ：     2022/04/24
-------------------------------------------------
"""
description_latest=f"""
- 作者： [@chinobing](https://github.com/chinobing/)

- 来源：`https://36kr.com/information/web_news/`
- 参数：没有
"""
@kr.get("/latest",
              summary="36kr-资讯",
              description=description_latest)
# @cached()
async def latest(filters=Depends(filter_keywords)):
    url = 'https://36kr.com/information/web_news/'

    fake = Faker()
    FAKE_HEADERS = {'Host':'36kr.com', 'User-Agent':fake.user_agent()}

    response = await fetch(url, headers=FAKE_HEADERS)
    data_text = response.re(r'<script>window.initialState=(.*?)</')[0]
    str_data = "".join(data_text)
    json_data = json.loads(str_data)
    itemList = json_data['information']['informationList']['itemList']

    links = []
    for item in itemList:
        link = 'https://36kr.com/p/' + str(item['itemId'])
        links.append(link)

    sub_responses = await fetch(links, headers=FAKE_HEADERS, cache_enabled=True)
    items_list = []
    for sub_re in sub_responses:
        title = sub_re.xpath('//h1[contains(@class,"article-title")]//text()').get()
        link = sub_re.xpath('//meta[@name="og:url"]/@content').get()
        date = sub_re.xpath('//span[contains(@class,"item-time")]//text()').getall()[1]
        pub_date = datetime.strptime(date,'%Y-%m-%d %H:%M')
        content = sub_re.xpath('//div[contains(@class,"articleDetailContent")]/node()').getall()
        description = "".join(content)

        _item = Item(title=title, link=link, description=description, pub_date=pub_date)
        _filter = filter_content(_item, filters)
        if _filter:
            items_list.append(_item)

    items_list = filter_content(items_list, filters)
    feed_data = {
        'title': '36kr-资讯',
        'link': url,
        'description': "",
        'item': items_list,
    }
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)


