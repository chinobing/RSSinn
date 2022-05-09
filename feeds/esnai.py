from fastapi import APIRouter, Depends, Query
from typing import Optional
from models.utils import DEFAULT_HEADERS, fetch, filter_keywords, filter_content
from models.decorator import cached
from fastapi_rss import RSSFeed, RSSResponse, Item

esnai = APIRouter()

"""
-------------------------------------------------
   Description :     会计视野论坛
   Modified_date：   2022/04/19
-------------------------------------------------
"""
description=f"""
- 作者： [@chinobing](https://github.com/chinobing/)

- 来源：`https://bbs.esnai.com/`
- 参数：**cat**， **include_keywords**， **exclude_keywords**
- 路由： `/esnai?cat=[]&include_keywords=[]&exclude_keywords=[]`
- Tips：对于cpa业务探讨(`?cat=7`)，可以选择包含关键字【`chenyiwei-aegis-fanxu7788-nikankan-henry204618-复制忍者卡卡西`】
"""
@esnai.get("/", summary='会计视野论坛', description=description)
@cached()
async def bbs_esnai(cat:Optional[int] = Query(None, description="输入子论坛数字，如https://bbs.esnai.com/forum-7-1.html，则输入`7`"),
                    filters=Depends(filter_keywords)):
    url = 'https://bbs.esnai.com/forum-{}-1.html'

    def parse(post):
        item = {}
        item['title'] = post.xpath(".//th[@class='new']//a[@class='s xst']//text()").get()
        link = post.xpath(".//th[@class='new']/a[@class='s xst']/@href").get()
        item['link'] = f'https://bbs.esnai.com/{link}'
        # item['description'] = ''
        authors = post.xpath(".//td[@class='by']/cite/a//text()").getall()
        item['author'] = ', '.join(str(x) for x in set(authors))
        return item

    #如果cat参数为空，则返回子论坛“CPA业务探讨”
    link = url.format(cat) if cat else 'https://bbs.esnai.com/forum-7-1.html'

    tree = await fetch(link, headers=DEFAULT_HEADERS)
    posts = tree.xpath("//tbody[contains(@id,'normalthread')]")
    items = list(map(parse, posts))
    items_list = []
    for _item in items:
        item = Item(title=_item['title'], link=_item['link'], author=_item['author'])
        _filter = filter_content(item, filters)
        if _filter:
            items_list.append(item)

    feed_data = {
        'title': '中国会计视野论坛',
        'link': 'https://bbs.esnai.com/',
        'description': "",
        'item': items_list,
    }
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)
