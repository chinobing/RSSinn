import logging
import requests
from typing import Optional
from freeproxy import freeproxy

fp_client = freeproxy.FreeProxy()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

class ProxyChecker:
    logger = logging.getLogger(__name__)

    @classmethod
    def proxy(cls,
              url: Optional[str]=None):
        proxy = list(fp_client.getrandomproxy().values())[0]

        if url is None:
            url = "http://www.baidu.com"
        try:
            cls.logger.info('get proxy ...')
            ip = {"http": "http://" + proxy, "https": "https://" + proxy}
            r = requests.get(url, proxies=ip, headers=headers, timeout=1)
            cls.logger.info(r.status_code)
            if r.status_code == 200:
                return proxy
        except:
            cls.logger.info('get proxy again ...')
            return cls.proxy()
