import time
from datetime import datetime

import requests

from database.bills import db_add_bills
from log import logger
from simulate.config.const import URL_DDBK_CHECK_BILLS, PAGE_SIZE, DEFAULT_HEADER, SECONDS_PER_DAY, \
    PATH_DDBK_COOKIES
from simulate.utils.io import json_load


def gen_params(date_start: int, page_number: int) -> dict:
    return {
        "orderType": 0,
        "afterSaleType": 0,
        "remarkStatus": -1,
        "urgeShippingStatus": -1,
        "groupStartTime": date_start,
        "groupEndTime": date_start + SECONDS_PER_DAY,
        "pageNumber": page_number,
        "pageSize": PAGE_SIZE
    }


def get_bills_of_day(date_start):
    def get_bills(date_start, page_number):
        nonlocal cnt
        bills = s.post(URL_DDBK_CHECK_BILLS, json=gen_params(date_start, page_number)).json()  # type: dict
        assert bills["success"] is True and bills["errorCode"] == 0 and bills["errorMsg"] == "成功", bills
        cnt = bills['result']['totalItemNum']
        # 需要对文档做一些hook，预处理一些文字输入
        docs = bills["result"]["pageItems"]
        # insert_many 时不能插入空列表
        if len(docs):
            docs_accum = (page_number - 1) * PAGE_SIZE + len(docs)
            # db_add_bills 里已经对bill做了一些预处理
            db_add_bills(docs)
            logger.info(f"{date_str}订单下载进度: ({docs_accum} / {cnt})")
        elif page_number == 1:
            logger.info(f"{date_str}没有订单~")
        
        # 速度控制在1秒实测是可以的，0.5秒不行
        if len(docs) == PAGE_SIZE:
            time.sleep(1)
            get_bills(date_start, page_number + 1)
    
    s = requests.Session()
    s.headers = DEFAULT_HEADER
    s.cookies.set("PASS_ID", json_load(PATH_DDBK_COOKIES)["PASS_ID"])
    date_str = datetime.fromtimestamp(date_start).strftime("%m月%d日")
    logger.info("fetching date: " + date_str)
    cnt = 0
    get_bills(date_start, 1)
    return cnt
