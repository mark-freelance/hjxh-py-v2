import time
from functools import partial

import pandas as pd
from fastapi import APIRouter, Depends, Query

from database.mongodb_client import db
from database.mongodb_query import AjaxResult, db_query
from settings import COLL_ORDERS, DEFAULT_MALL_ID, DEFAULT_GOODS_ID, SECONDS_EACH_DAY, EXCLUDE_ORDER_STATUS_LIST

orders_router = APIRouter(tags=['订单系统'], prefix='/orders')

coll_orders = db[COLL_ORDERS]


@orders_router.get('/', summary='获取所有订单信息')
def get_orders(dep: AjaxResult = Depends(partial(db_query, 'orders'))):
    return dep


@orders_router.get('/rank', summary='获取所有店铺下不同商品的订单量排序')
def get_panorama_of_orders(days: int = 7) -> AjaxResult:
    agg = coll_orders.aggregate([
        {
            "$match": {
                "order_time": {"$gt": time.time() - days * SECONDS_EACH_DAY},
                "order_status_str": {"$not": {"$in": EXCLUDE_ORDER_STATUS_LIST}}
            }
        },
        {
            "$group": {
                "_id": {
                    "mall_id": "$mallId",
                    "goods_id": "$goods_id",
                },
                "goods_name": {
                    "$first": "$goods_name"
                },
                "count": {
                    "$sum": 1
                }
            }
        },
        {
          "$sort": {
              "count": -1
          }
        },
        {
            "$replaceRoot": {
                "newRoot": {
                    "$mergeObjects": [
                        {
                            "mall_id": "$_id.mall_id",
                            "goods_id": "$_id.goods_id",
                        },
                        "$$ROOT"
                    ]
                }
            }
        },
        {
            "$project": {
                "_id": 0
            }
        }
    ])
    return {
        "success": True,
        "result": {
            "items": list(agg)
        }
    }


@orders_router.get('/analysis', summary='基于订单系统的单品分析')
def analyze_orders_of_goods(
    mall_id: int = DEFAULT_MALL_ID,
    goods_id: int = DEFAULT_GOODS_ID,
    days: int = 7
) -> AjaxResult:
    agg = coll_orders.aggregate([
        {
            "$match": {
                "mallId": mall_id,
                "goods_id": goods_id,
                "order_time": {"$gt": time.time() - days * SECONDS_EACH_DAY},
                "order_status_str": {"$not": {"$in": EXCLUDE_ORDER_STATUS_LIST}}
            }
        },
        {
            "$addFields": {
                "date": {
                    "$dateToString": {
                        "date": {
                            "$toDate": {
                                "$multiply": [
                                    "$order_time",
                                    1000
                                ]
                            }
                        },
                        "format": "%Y-%m-%d"
                    }
                }
            }
        },
        {
            "$group": {
                "_id": {
                    "date": "$date",
                    "sku": "$spec"
                },
                "goods_number": {
                    "$sum": "$goods_number"
                },
                "goods_amount": {
                    "$sum": "$goods_amount"
                }
            }
        },
        {
            "$replaceRoot": {
                "newRoot": {
                    "$mergeObjects": [
                        {
                            "date": "$_id.date",
                            "sku": "$_id.sku"
                        },
                        "$$ROOT"
                    ]
                }
            }
        },
        {
            "$project": {
                "_id": 0
            }
        }
    ])
    
    items = list(agg)
    
    def get_pivot(key: str) -> pd.DataFrame:
        df = pd.DataFrame(items) \
        .pivot_table(values=key, index='date', columns='sku') \
        .sort_index(ascending=False) \
        .reset_index() \
        .fillna(0)  # important ! can't export to dict with nan
        
        # refer: python - how do I insert a column at a specific column index in pandas? - Stack Overflow - https://stackoverflow.com/questions/18674064/how-do-i-insert-a-column-at-a-specific-column-index-in-pandas
        df.insert(1, 'sum', df.sum(axis=1))
        return df
    
    df_volume = get_pivot('goods_number')
    df_amount = get_pivot('goods_amount')
    
    return {
        "success": True,
        "result": {
            "columns": df_volume.columns.tolist(),
            'volume': df_volume.to_dict(orient='records'),
            'amount': df_amount.to_dict(orient='records')
        }
    }
