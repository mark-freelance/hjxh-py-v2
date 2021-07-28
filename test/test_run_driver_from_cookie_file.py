import os

from simulate.config.const import DATA_PATH, URL_DDBK_HOME
from simulate.utils.driver import driver
from simulate.utils.io import json_load

'''
在设置cookies前，先访问需要登录的地址，然后设置cookies登录跳转，就OK了。
reference: https://www.cnblogs.com/deliaries/p/14121204.html
'''
driver.get(URL_DDBK_HOME)

cookie_list = json_load(os.path.join(DATA_PATH, "ddbk-COOKIE-list.json"))
for cookie in cookie_list:
    driver.add_cookie({"name": cookie["name"], "value": cookie["value"]})

driver.get(URL_DDBK_HOME)
