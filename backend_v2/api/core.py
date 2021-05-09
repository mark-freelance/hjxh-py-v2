import time
from collections import defaultdict
from typing import Any, List, TypedDict

from fastapi import APIRouter, Query
from pydantic import BaseModel

from api.orders import coll_orders
from settings import DEFAULT_GOODS_ID, SECONDS_EACH_DAY, EXCLUDE_ORDER_STATUS_LIST

core_router = APIRouter(prefix='/core', tags=['核心API'])


class BaseResponseModel(BaseModel):
    success: bool = False
    result: Any
    msg: str = ""


class BaseItemModel(TypedDict, total=False):
    date: str


def query_sku_of_goods(id: int, days: int) -> List[BaseItemModel]:
    return coll_orders.aggregate([
        {
            "$match": {
                "goods_id": id,
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
                    "spec": "$spec"
                },
                "goods_number": {"$sum": "$goods_number"},
                "goods_amount": {"$sum": "$goods_amount"}
            }
        },
        {
            "$unwind": "$_id.spec"
        }
    ])


def query_refund_of_goods(id: int, days: int) -> List[BaseItemModel]:
    return coll_orders.aggregate([
        {
            "$match": {
                "goods_id": id,
                "order_time": {"$gt": time.time() - days * SECONDS_EACH_DAY},
                "order_status_str": {"$regex": '退款成功'}
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
                "_id": "$date",
                "date": {"$first": "$date"},
                "goods_number": {"$sum": "$goods_number"},
                "goods_amount": {"$sum": "$goods_amount"}
            }
        }
    ])


@core_router.get('/query', summary='一次性获取某个商品的所有信息（日频）', response_model=BaseResponseModel)
def core_query_goods(
    id: int = Query(DEFAULT_GOODS_ID, description='商品ID'),
    days: int = Query(14, description='从今天零点起往前总计日数'),
    with_sku: bool = Query(True, description='包含SKU的交易细分数据'),
    with_refund: bool = Query(True, description="包含退款相关数据"),
    with_advertise: bool = Query(True, description='包含多多推广、多多场景、放心推等推广数据'),
    with_goods_detail: bool = Query(True, description='包含商品明细数据'),
    with_goods_comments: bool = Query(True, description='包含商品评价数据'),
    with_mall_info: bool = Query(True, description="包含销售该商品的店铺信息")
):
    result = defaultdict(dict)
    if with_sku:
        for item in query_sku_of_goods(id, days):
            result[item.pop("_id")]["sku"] = item
    if with_refund:
        for item in query_refund_of_goods(id, days):
            result[item.pop('_id')]['refund'] = item
    
    return {"result": result, "success": True}
