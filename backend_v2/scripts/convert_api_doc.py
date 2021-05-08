from pprint import pprint

import requests

from settings import DEFAULT_USER_AGENT

url = 'https://open.pinduoduo.com/application/document/api?id=pdd.ad.api.unit.query.list'


headers = {
    "User-Agent": DEFAULT_USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}
data = requests.get(url, headers=headers)


print(data.text)

"""
失败了！需要启用javascript！
"""