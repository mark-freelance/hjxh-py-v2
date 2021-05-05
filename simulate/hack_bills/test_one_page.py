"""
测试某页的50条
"""
from datetime import datetime

from simulate.config.const import PAGE_SIZE, URL_DDBK_CHECK_BILLS
from simulate.hack_bills.core import s

if __name__ == '__main__':
    date_start = int(datetime(2021, 4, 23, 0, 0).timestamp())
    date_end = int(datetime(2021, 4, 24, 0, 0).timestamp())
    page_number = 12
    params = {
        "orderType": 0,
        "afterSaleType": 0,
        "remarkStatus": -1,
        "urgeShippingStatus": -1,
        "groupStartTime": date_start,
        "groupEndTime": date_end,
        "pageNumber": page_number,
        "pageSize": PAGE_SIZE
    }
    bills = s.post(URL_DDBK_CHECK_BILLS, json=params).json()
    docs = bills['result']['pageItems']
