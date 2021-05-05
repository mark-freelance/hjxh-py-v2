import time
from datetime import datetime

import numpy as np
import pandas as pd
from pymongo.errors import DuplicateKeyError

from db.client import db

coll_bills = db['bills']

BILLS_PROJECTIONS = ['goods_id', "goods_number", 'spec', 'order_time']


def hook_bill(bill: dict):
    """
    4月23日，第47条的`receiveName`会报错，因为有非法字符`\\uxxxx`
    所以需要预处理
    :param bill:
    :return:
    """
    bill["update_time"] = time.time()
    bill["receive_name"] = bill["receive_name"].encode('unicode-escape').decode('ascii')
    # _id就是用order_sn
    bill["_id"] = bill["order_sn"]
    return bill


def db_add_bill(bill):
    try:
        coll_bills.insert_one(hook_bill(bill))
    except DuplicateKeyError:
        pass


def db_add_bills(bills):
    coll_bills.insert_many([hook_bill(bill) for bill in bills])


def db_fetch_bills(*func_filter, skip=0, limit=10):
    if func_filter is None:
        func_filter = {}
    return list(coll_bills.find(*func_filter).skip(skip).limit(limit))


def db_fetch_bills_of_id(goods_id: int, limit: int = 10):
    bills_docs = db_fetch_bills({"goods_id": goods_id}, dict((i, 1) for i in BILLS_PROJECTIONS), limit=limit)
    df_bills = pd.DataFrame(bills_docs)
    df_bills['date'] = df_bills['order_time'].apply(lambda x: datetime.fromtimestamp(x).date())
    dfp = df_bills.pivot_table(index=['spec'], columns=['date'], values=['goods_number'], aggfunc=np.sum,
                               fill_value=0).droplevel(level=0, axis=1)
    dfp.sort_index(axis=1, ascending=False, inplace=True)
    cols = list(dfp.columns.map(lambda x: x.strftime("%m-%d")))
    def gen_item(i, j):
        d = {'名称': i}
        d.update(zip(cols, j))
        return d
    return [gen_item(i, j) for (i, j) in dfp.iterrows()]