from fastapi import APIRouter
from models.utils import fetch
from fastapi_rss import RSSFeed, RSSResponse, Item
from typing import Optional
from datetime import datetime
import json

stock_exchange = APIRouter()

"""
-------------------------------------------------
   Description :     深交所 - 具体项目动态
   Created at  ：    2022/04/27
   Modified at :     N/A
-------------------------------------------------
"""
szse_ipo_description=f"""
- 作者： [@chinobing](https://github.com/chinobing/)

- 来源：`http://listing.szse.cn/projectdynamic/ipo/index.html`
- 参数：**id**, `IPO申报项目的ID`
- 路由： `/szse/ipo?id=[]`， 如`/szse/ipo?id=1001583`
"""
@stock_exchange.get("/szse/ipo",
            summary="深交所 - IPO项目动态",
            description=szse_ipo_description)
async def szse_ipo(id:Optional[int]= None):
    if id is None or not id:
        id = 1001583

    url = f"http://listing.szse.cn/api/ras/projectrends/details?id={id}"
    link = f"http://listing.szse.cn/projectdynamic/ipo/detail/index.html?id={id}"

    response= await fetch(url)
    json_data = json.loads(response)
    itemList = json_data['data']

    title = f"[{itemList['prjst']}, {itemList['updtdt']}]{itemList['cmpnm']}"
    pub_date = datetime.strptime(itemList['updtdt'], '%Y-%m-%d')

    description = f"状态：{itemList['prjst']}<br>" \
                  f"最新进度：{itemList['prjprog']}<br>" \
                  f"行业：{itemList['csrcind']}<br>" \
                  f"保荐机构：{itemList['sprinsts']}<br>" \
                  f"律师事务所：{itemList['lawfm']}<br>" \
                  f"会计师事务所：{itemList['acctfm']}<br>" \
                  f"募集金额：{itemList['maramt']}亿元<br>" \

    _item = Item(title=title, link=link, description=description, pub_date=pub_date)

    feed_data = {
        'title': f"证监会 - {itemList['cmpnm']}-IPO项目动态",
        'link': link,
        'description': "",
        'item': [_item],
    }
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)
