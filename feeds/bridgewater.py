from fastapi import APIRouter
from models.utils import fetch
from fastapi_rss import RSSFeed, RSSResponse, Item
from faker import Faker
from datetime import datetime

bridgewater = APIRouter()


description="""
- 作者： [@chinobing](https://github.com/chinobing/)

- 来源：`https://www.bridgewater.com/research-and-insights/`
- 参数：没有
"""

@bridgewater.get("/research/",
              summary="桥水（Bridgewater)研究与观察",
              description=description)
async def research():
    url = 'https://www.bridgewater.com/research-and-insights'

    fake = Faker()
    FAKE_HEADERS = {'User-Agent':fake.user_agent()}
    tree = await fetch(url, headers=FAKE_HEADERS)
    posts = tree.xpath("//div[@class='PromoC-content']")

    items_list = []
    for post in posts:
        title = post.xpath(".//div[@class='PromoC-title']/a//text()").get()
        link= post.xpath(".//div[@class='PromoC-title']/a/@href").get()
        author = post.xpath(".//div[@class='PromoC-author']//text()").get()
        description = post.xpath(".//div[@class='PromoC-description']//text()").get()
        date = post.xpath(".//div[@class='PromoC-date']//text()").get()
        if date:
            if ',' not in date:
                pub_date = datetime.strptime(date, '%B %Y')
            else:
                # pub_date = datetime.strptime(date, '%B %-d, %Y') #On Windows, you should use # to avoid the zero-padding (it replaces the - on Unix systems).
                day = date.split(' ')[1].replace(',', '')
                day_cv = day.zfill(2)
                date = date.replace(day,day_cv, 1)
                pub_date = datetime.strptime(date,'%B %d, %Y')
        else:
            pub_date = datetime.now()

        _item = Item(title=title, link=link, author=author,description=description, pub_date=pub_date)
        items_list.append(_item)

    feed_data = {
        'title': '桥水（bridgewater）研究与观察',
        'link': url,
        'description': "",
        'item': items_list,
    }
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)

