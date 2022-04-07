from settings import upptime_status_url


def add_upptime_status(site=''):
    if not site or not upptime_status_url:
        return "暂无；请设置站点名称 和 upptime_status_url的网址"
    if upptime_status_url:
        url = f'![Uptime](https://img.shields.io/endpoint?url={upptime_status_url}/api/_/uptime.json)'
    upptime_status = url.replace('_',site)
    return upptime_status