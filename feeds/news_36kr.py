from fastapi import APIRouter
from models.utils import fetch
from models.proxy_checker import ProxyChecker
from fastapi_rss import RSSFeed, RSSResponse, Item
from faker import Faker
from datetime import datetime
from models.decorator import cached
import json

kr = APIRouter()

"""
-------------------------------------------------
   Description :     36kr-实时快讯
   Modified_date：   2022/04/19
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
@kr.get("/latest/",
              summary="36kr-资讯",
              description=description_latest)
@cached()
async def latest():
    url = 'https://36kr.com/information/web_news/'

    fake = Faker()
    FAKE_HEADERS = {'Host':'36kr.com', 'User-Agent':fake.user_agent()}

    proxy = ProxyChecker.proxy(url)
    response = await fetch(url, headers=FAKE_HEADERS, proxy={"proxy_server": proxy})
    data_text = response.re(r'<script>window.initialState=(.*?)</')[0]
    str_data = "".join(data_text)
    json_data = json.loads(str_data)

    itemList = json_data['information']['informationList']['itemList']
    print(itemList)
    links = []
    for item in itemList:
        link = 'https://36kr.com/p/' + str(item['itemId'])
        links.append(link)

    sub_responses = await fetch(links, headers=FAKE_HEADERS, cache_enabled=True, proxy={"proxy_server": proxy})
    items_list = []
    for link, sub_re in zip(links,sub_responses):
        title = sub_re.xpath('//h1[contains(@class,"article-title")]//text()').get()
        date = sub_re.xpath('//span[contains(@class,"item-time")]//text()').getall()[1]
        pub_date = datetime.strptime(date,'%Y-%m-%d %H:%M')
        content = sub_re.xpath('//div[contains(@class,"articleDetailContent")]/node()').getall()
        description = "".join(content)

        _item = Item(title=title, link=link, description=description, pub_date=pub_date)
        items_list.append(_item)

    feed_data = {
        'title': '36kr-资讯',
        'link': url,
        'description': "",
        'item': items_list,
    }
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)


