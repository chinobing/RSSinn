import logging
import requests
from models.read_yaml import parsing_yaml
proxy_pool_address = parsing_yaml()['fetch_proxy_settings']['proxy_pool']['server']



class ProxyChecker:
    logger = logging.getLogger(__name__)

    @classmethod
    def proxy(cls):
        proxy = requests.get(f"{proxy_pool_address}/get").json().get("proxy")
        try:
            cls.logger.info('get proxy ...')
            ip = {"http": "http://" + proxy, "https": "https://" + proxy}
            r = requests.get("http://www.baidu.com", proxies=ip, timeout=4)
            cls.logger.info(r.status_code)
            if r.status_code == 200:
                return proxy
        except:
            cls.logger.info('get proxy again ...')
            cls.delete_proxy(proxy)
            return cls.proxy()

    @classmethod
    def delete_proxy(cls, proxy):
        requests.get(f"{proxy_pool_address}/delete/?proxy={proxy}")
