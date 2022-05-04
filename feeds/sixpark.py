from fastapi import APIRouter
from models.utils import fetch
from fastapi_rss import RSSFeed, RSSResponse, Item
from datetime import datetime

sixpark = APIRouter()

"""
-------------------------------------------------
   Description :     留园网（6park.com)
   Created_at：      2022/05/04
-------------------------------------------------
"""
search_description=f"""
- 作者： [@chinobing](https://github.com/chinobing/)

- 来源：`https://www.6park.com/search.php?keyword=[]&sa=留园搜索`
- 参数：没有
"""
@sixpark.get("/search",
              summary="留园网（6park.com) 搜索",
              description=search_description)
async def search(kw):
    url = f'https://www.6park.com/search.php?keyword={kw}&sa=留园搜索'

    tree = await fetch(url)
    posts = tree.xpath("//div[@class='search-content']/ul/li")
    print(tree)

    items_list = []
    for post in posts[:5]:
        _title = post.xpath(".//p[@class='lf']//text()").getall()
        title = "".join(_title)

        date = post.xpath(".//p[@class='lr']//text()").get()
        pub_date = datetime.strptime(date, '%Y-%m-%d %H:%M')

        link= post.xpath(".//a/@href").get()

        detail_post = await fetch(link, cache_enabled=True)
        content = detail_post.xpath("//td[@class='show_content']/pre/node()").getall()
        description = "".join(content)

        _item = Item(title=title, link=link, description=description, pub_date=pub_date)
        items_list.append(_item)

    feed_data = {
        'title': f"留园网（6park.com) 搜索 {kw}",
        'link': url,
        'description': f"留园网（6park.com) 搜索 {kw}",
        'item': items_list,
    }
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)

