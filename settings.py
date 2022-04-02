from fastapi import FastAPI



#设置upptime status的路径， https://upptime.js.org/， 地址为https://cdn.jsdelivr.net/gh/github账户/repo名称@master
upptime_status_url = 'https://cdn.jsdelivr.net/gh/chinobing/upptime-rssinn@master'



#设置网站的基本信息
def app_settings() -> FastAPI():
    return {
        'title': 'RSS inn - RSS小黑屋',
        'description': 'Powered by FastAPI',
        'swagger_ui_parameters': {
                                "defaultModelsExpandDepth": -1,
                                "filter": True
                                  },
    }

