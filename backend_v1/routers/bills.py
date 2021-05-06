from datetime import datetime, date, timedelta
from typing import List, Optional

import numpy as np
import pandas as pd
from fastapi import APIRouter

from database.bills import BILLS_PROJECTIONS, coll_bills
from api.models.base import MongoOutModel

api_bills = APIRouter(prefix="/bills", tags=["订单数据"])


class BillOut(MongoOutModel):
    order_sn: str
    goods_name: Optional[str]
    spec: Optional[str]
    goods_number: Optional[int]
    order_amount: Optional[int]
    order_status_str: str
    order_time: int
    nickname: str
    created_at: Optional[int]
    receive_name: Optional[str]
    thumb_url: Optional[str]


@api_bills.get("/", response_model=List[BillOut])
def get_bill(skip: int = 0, limit: int = 10):
    items = list(coll_bills.find(skip=skip, limit=limit))
    # logger.info(items)
    return items


def get_ts_from_date(d: date) -> int:
    return int(datetime.fromordinal(d.toordinal()).timestamp())


@api_bills.get('/pivot')
def get_pivoted_bills(goods_id: int = 221058511472, limit: int = 3000, days: int = 7):
    bills_docs = coll_bills.find({"goods_id": goods_id, "order_time": {
        '$gt': get_ts_from_date(date.today() - timedelta(days=days))}}, BILLS_PROJECTIONS, limit=limit)
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
