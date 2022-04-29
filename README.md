# 介绍
RSSinn是一个基于python FastAPI 的RSS生成器。 利用了FastAPI 自动生成交互式文档、支持 asyncio等特点， 减少了手动创建文档的工作量。

## 功能说明
### fetch
用于解释url，返回
1. 带Selector的html原始数据，可用于XPath或者CSS
2. json

**参数**：
1. proxy: {"proxy_server":"", "proxy_username":"", "proxy_password":""} 
2. fetch_js: True or False #利用playwright获取js加载的网页内容
3. cache_enabled:  True or False #是否cache缓存

```python
#引入
from models.utils import fetch

#使用
response = await fetch(url)

```





### RSS过滤
rssinn集成了内容过滤功能

1. **inculde_keywords**：包含指定的关键字；
2. **exclude_keywords**：不含指定关键字。

引入方式
```python
from fastapi import APIRouter, Depends
from models.utils import filter_keywords, filter_content
```
使用方式， 具体可参考`feeds/toscrape.py/`中的`quotes_with_filter`例子
```python
demo = APIRouter()

@demo.get("/demo_with_filter/",
              summary="获取带指定关键字的所有quotes",
              description="`inculde_keywords`：包含指定的关键字；`exclude_keywords`：不含指定关键字；")
async def demo_with_filter(filters=Depends(filter_keywords)):
    #获取feed代码
    ......
    
    items_list = []
    for _item in items:
        item = Item(title=_item['author'], author=_item['author'], description=_item['description'])
         # 在item项中添加下面代码即可即可
        _filter = filter_content(item, filters)
        if _filter:
            items_list.append(item)

    feed_data = {
        'title': 'toscrape with content filter',
        'link': 'toscrape.com',
        'description': "",
        'item': items_list,
    }
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)

```
路由: `https://localhost:28085/demo?include_keywords=[]&exclude_keywords=[]`

### proxy
这里提供了两种proxy方式
- 第一种， 直接在`setting.yaml`中填写相应的proxy
- 第二种， 在feed脚本中单独添加, 利用了[CharlesPikachu freeproxy](https://github.com/CharlesPikachu/freeproxy) 库
```python
#引入
from models.proxy_checker import ProxyChecker

#feed的目标地址
url=“http://example.com”

#返回proxy url
proxy = ProxyChecker.proxy(url)
response = await fetch(url,  proxy={"proxy_server": proxy})

```

### upptime
> Upptime (https://upptime.js.org) is the open-source uptime monitor and status page, powered entirely by GitHub Actions, https://github.com/upptime/upptime

请在`setting.yaml`中填写相应的`github username` 和 `repo`

**demo**： https://www.rssinn.com/upptime

### redis or in-memory cache
由于过度实时加载feeds会导致服务器资源紧张， 这里引入了cache

请在`setting.yaml`中填写相应的cache时间(秒)和方式（redis or in-memory)

**使用方式一：cache整个route返回的结果**

直接引入`@cached()`即可
```python
from models.decorator import cached

demo = APIRouter()

@demo.get("/example/")
@cached() 
async def example():
    pass
```

**使用方式二：cache fetch返回的原始html**

在`fetch`中添加`cache_enabled=True)`即可
```python
raw_html = await fetch(url, cache_enabled=True)
```
这样做的目的是：模拟增量式抓取和数据更新，防止被目标网站封禁

# 贡献RSS Feed方法
1. 首先fork这个repository
2. 在`feeds`文件夹中创建新的`py`脚本，并将对应的APIRoute路由的名称添加到`__init__.py`， 将对应的APIRoute路由的名称同时添加到根目录的`routes.py`
4. 提pr


# 部署|Deployment
## 直接部署
下载 `RSSinn` 的源码
```
git clone https://github.com/chinobing/RSSinn.git
cd RSSinn
```
安装依赖库
```
pip install -r requirements.txt

国内的运行：
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
运行playwright
```commandline
playwright install
```

运行项目
```
uvicorn run:app --host 0.0.0.0 --port 28085
```

注：
1. **requires python 3.8**
## PDM部署（Linux)
> [PDM (Python Development Manager)](https://pdm.fming.dev/) 是一个新的 Python 项目管理器，类似Pipenv 和 Poetry。

下载 `RSSinn` 的源码
```
git clone https://github.com/chinobing/RSSinn.git
cd RSSinn
```
安装PDM
```
pip install --user pdm
```
执行` pdm init `初始化项目，并填写项目信息， 最后生成` pyproject.toml` 配置文件
- 是否要上传 PyPI
- 依赖的 Python 版本
- License 类型
- 作者信息
- 邮箱信息
- 是否导入`requirements.txt`

将`pdm命令`加入path
```
export PATH=/root/.local/bin:$PATH
```

安装/更新项目依赖库
```
pdm update
```
运行playwright
```commandline
pdm run playwright install
```
后台运行项目命令
```commandline
nohup pdm run uvicorn run:app --host 0.0.0.0 --port 28085 > log.txt 2>&1 &
```

调试debug命令
```commandline
pdm run uvicorn run:app --host 0.0.0.0 --port 28085 --reload --debug
```

关闭进程命令
```commandline
fuser -n tcp -k 28085
```

注：
1. **requires  Python 3.8**


## Docker 部署
制作镜像文件
```
docker build -t "rssinn" .
```

创建docker容器 

```
docker run -dit -p 28085:28085 rssinn
```

