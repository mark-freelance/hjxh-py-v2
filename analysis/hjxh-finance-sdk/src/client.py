import time

import requests

from .get_sign import get_sign


class Client:
    
    def __init__(self, sid: str, app_key: str, app_secret: str):
        self.sid = sid
        self.app_key = app_key
        self.app_secret = app_secret
    
    def query(self, url: str, params: dict = None):
        if not params:
            params = {
                "page_no": 1
            }
        params.update({
            'sid': self.sid,
            'appkey': self.app_key,
            "timestamp": str(int(time.time()))
        })
        params['sign'] = get_sign(params, self.app_secret)
        return requests.post(url, data=params).json()
