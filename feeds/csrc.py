from fastapi import APIRouter
from models.utils import fetch
from fastapi_rss import RSSFeed, RSSResponse, Item
from typing import Optional
from datetime import datetime

csrc = APIRouter()

"""
-------------------------------------------------
   Description :     证监会 - 辅导企业基本情况
   Created at  ：    2022/04/23
   Modified at :     2022/04/25
-------------------------------------------------
"""
fudao_description=f"""
- 作者： [@chinobing](https://github.com/chinobing/)

- 来源：`http://www.csrc.gov.cn/`
- 参数：**kw**, 包括: 北京、天津、河北、山西、内蒙古、辽宁、吉林、黑龙江、上海、江苏、浙江、安徽、福建、江西、山东、河南、湖北、湖南、广东、广西、海南、重庆、四川、贵州、云南、西藏、陕西、甘肃、青海、宁夏、新疆、深圳、大连、宁波、厦门、青岛
- 路由： `/csrc/?fudao=[]`， 如`/csrc/?fudao=深圳`
"""
@csrc.get("/fudao",
            summary="证监会 - 辅导企业基本情况",
            description=fudao_description)
async def fudao(kw:Optional[str]=None):
    keywords='北京天津河北山西内蒙古辽宁吉林黑龙江上海江苏浙江安徽福建江西山东河南湖北湖南广东广西海南重庆四川贵州云南西藏陕西甘肃青海宁夏新疆深圳大连宁波厦门青岛'

    if kw is None or kw not in keywords:
        kw=""
        url = 'http://eid.csrc.gov.cn/102510/index_f.html?order=filingDate'
    else:
        url = f'http://eid.csrc.gov.cn/102510/index_f.html?keyWord={kw}&order=filingDate'

    table_data= await fetch(url)

    items_list = []
    table_tr = table_data.xpath("//table//tr")
    columns = table_tr[0].xpath(".//th//text()").getall()

    for tr in table_tr[1:]:
        record = []
        trs = tr.xpath(".//td")
        onclick = tr.xpath(".//@onclick").get().split(',')
        print(onclick)
        pdf_link = f"http://eid.csrc.gov.cn/{onclick[0][14:-1]}"
        pdf_title = tr.xpath(".//@title").get()
        for each in trs[1:]:
            text = each.xpath("normalize-space(.//text())").get()
            record.append(text)
        _title = record[0] if record[0] else pdf_title
        title = f"[{record[3]}]{_title}"
        date = record[2]
        pub_date = datetime.strptime(date, '%Y-%m-%d')

        description=''
        for col, txt in zip(columns,record):
            description +=f"{col}: {txt}<br>"
        description += f"报告文件：<a href='{pdf_link}'>{pdf_title}</a>"

        _item = Item(title=title, link=pdf_link, description=description, pub_date=pub_date)
        items_list.append(_item)

    feed_data = {
        'title': f'证监会 - {kw}辅导企业基本情况',
        'link': url,
        'description': "",
        'item': items_list,
    }
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)
