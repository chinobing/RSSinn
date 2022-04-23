from fastapi import APIRouter, HTTPException
from models.utils import fetch
from fastapi_rss import RSSFeed, RSSResponse, Item
from typing import Optional
from datetime import datetime
import json

csrc = APIRouter()

"""
-------------------------------------------------
   Description :     证监会 - 辅导企业基本情况
   Created at  ：    2022/04/23
-------------------------------------------------
"""
fudao_description=f"""
- 作者： [@chinobing](https://github.com/chinobing/)

- 来源：`http://www.csrc.gov.cn/`
- 参数：没有
"""
@csrc.get("/fudao",
            summary="证监会 - 辅导企业基本情况",
            description=fudao_description)
async def fudao(kw:Optional[str]=None):
    province = {"beijing": "1624bb2fa2a242ac88075d0e7e45c7c1",
                "tianjin": "6b1ce7c39d614be1b35ccc97b36ce7ce",
                "hebei": "bd19b84be46643639069edd3bf25c6be",
                "shanxi": "73a8638617d94565ac3bee3d63539e0e",
                "neimenggu": "c3bcfe67f7694eef84017c2a40146ba3",
                "liaoning": "99a834356b964bad8dfff253920e9384",
                "jilin": "340c4ee5e10a4e2c90a349ef85b11d8d",
                "heilongjiang": "0cd1bc21094845ac8bb65f05628969a6",
                "shanghai": "ad550f2caf5e4ae0b5be2ceb82b12794",
                "jiangsu": "c67207e5f2584dff982f50327d6c26ab",
                "zhejiang": "5bdc6f24a1ab42138d081c36c302e029",
                "anhui": "7585e935cada40f98ed828a48521a3c6",
                "fujian": "6aa3ae576a244fe4825b05f63dbf849c",
                "jiangxi": "163a10acddb746ebb57e422f42376c0a",
                "shandong": "9dd60245cc634a10996373459efe0b56",
                "henan": "850a7cfbd2954147a5f501f521b77c61",
                "hubei": "408f99a8022144bc826e328a73465ea6",
                "hunan": "ee3c58bd95834ca6aaf229c25b332cc7",
                "guangdong": "b6393302b8e548fead8ff4e54dc74799",
                "guangxi": "2cbff1c143434b38a98dca4fd6048929",
                "hainan": "6d4eae2594874c55bb9b5d98f925ceb0",
                "chongqing": "2ca84d4c44234868a0f5b8222e39a409",
                "sichuan": "5adda2664b1849d8ba3422ac8d0c86b0",
                "guizhou": "056e61c7e8324d089692ee36729b0670",
                "yunnan": "f081f2fa7abe470b86bc6e64f5e78e52",
                "tibet": "b623652a1caa4b1d9aef32f5c3bdf9d4",
                "shaanxi": "ac58e4d41c6242bf81b8e067e46f9d65",
                "gansu": "5818b08aa96b404e9305abe935efed5a",
                "qinghai": "a2bcb79e94a04b128420d62d36489f91",
                "ningxia": "947e776a4505457b8d142d2dabc8c8ac",
                "xinjiang": "0fcb6363eb74460b9358b5208f10c76c",
                "shenzhen": "9a2138b844a24aa7ab5dc936ba0f85c8",
                "dalian": "4c4664dfe8854034ab9f9ec3770fdd97",
                "ningbo": "61d28c49349543c5b69cd526d0d70394",
                "xiamen": "c2571faf49664707bcdae07ea27f45e1",
                "qingdao": "0aac3a415f4248539364ad7a8aa63600",
                }

    if kw is None or kw not in province:
        raise HTTPException(status_code=404, detail="请填写正确的【省/城市】对应的拼音")
    if kw in province:
        url = f'http://www.csrc.gov.cn/searchList/{province[kw]}?_isAgg=false&_isJson=true&_pageSize=18&_template=index&_rangeTimeGte=&_channelName=&page=1'
        str_data = await fetch(url)
        json_data = json.loads(str_data)
        data = json_data['data']['results']
        items_list = []
        for item in data:
            title = item['title']
            link = item['url']
            ctime = int(item['publishedTime'])/1000
            pub_date = datetime.fromtimestamp(ctime)
            if item['resList']:
                fileName = item['resList'][0]['fileName']
                filePath = item['resList'][0]['filePath']
                description = f"<a href=http://www.csrc.gov.cn{filePath}>{fileName}</a>"
            else:
                description = item['subTitle']

            _item = Item(title=title, link=link, description=description, pub_date=pub_date)
            items_list.append(_item)

        feed_data = {
            'title': f'证监会 - {kw}辅导企业基本情况',
            'link': url,
            'description': "",
            'item': items_list,
        }
        feed = RSSFeed(**feed_data)
        return RSSResponse(feed)



