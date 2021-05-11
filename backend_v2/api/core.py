import datetime
import time
from typing import Any, List, TypedDict

from fastapi import APIRouter, Query
from pydantic import BaseModel

from api.orders import coll_orders
from database.mongodb_client import db
from settings import DEFAULT_GOODS_ID, SECONDS_EACH_DAY, EXCLUDE_ORDER_STATUS_LIST, COLL_AD_SEARCH, COLL_AD_SCENE, \
    COLL_AD_FANGXIN, COLL_GOODS_LIST, COLL_GOODS_COMMENTS_DETAIL

core_router = APIRouter(prefix='/core', tags=['核心API'])


class BaseResponseModel(BaseModel):
    success: bool = False
    result: Any
    msg: str = ""


class BaseItemModel(TypedDict, total=False):
    date: str


def query_sku_of_goods(id: int, days: int, long_table=False) -> List[BaseItemModel]:
    pipes = [
        {
            "$match": {
                "goods_id": id,
                "order_time": {"$gt": time.time() - days * SECONDS_EACH_DAY},
                "order_status_str": {"$not": {"$in": EXCLUDE_ORDER_STATUS_LIST}}
            }
        },
        {
            '$addFields': {
                'date': {
                    '$dateToString': {
                        'date': {
                            '$toDate': {
                                '$multiply': [
                                    '$order_time', 1000
                                ]
                            }
                        },
                        'format': '%Y-%m-%d'
                    }
                }
            }
        },
        {
            '$project': {
                'goods_number': 1,
                'goods_amount': 1,
                'spec': 1,
                "date": 1,
            }
        },
    
    ]
    if not long_table:
        pipes.extend(
            [
                {
                    '$group': {
                        '_id': {
                            'date': '$date',
                            'spec': '$spec'
                        },
                        'goods_number': {
                            '$sum': '$goods_number'
                        },
                        'goods_amount': {
                            '$sum': '$goods_amount'
                        }
                    }
                },
                #  to list :
                {
                    '$group': {
                        '_id': '$_id.date',
                        'data': {
                            '$push': {
                                "spec": "$_id.spec",
                                'goods_number': '$goods_number',
                                'gooods_amount': '$goods_amount'
                            }
                        }
                    }
                },
                
                #  to dict :
                # {
                #     '$group': {
                #         '_id': '$_id.date',
                #         'data': {
                #             '$push': {
                #                 'k': '$_id.spec',
                #                 'v': {
                #                     'goods_number': '$goods_number',
                #                     'gooods_amount': '$goods_amount'
                #                 }
                #             }
                #         }
                #     }
                # },
                # {
                #     '$project': {
                #         'data': {
                #             '$arrayToObject': '$data'
                #         }
                #     }
                # },
            ]
        )
    return coll_orders.aggregate(pipes)


def query_total_of_goods(id: int, days: int) -> List[BaseItemModel]:
    return coll_orders.aggregate([
        {
            "$match": {
                "goods_id": id,
                "order_time": {"$gt": time.time() - days * SECONDS_EACH_DAY},
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
                },
                "isRefund": {
                    "$regexMatch": {
                        "input": "$order_status_str",
                        "regex": "退款成功"
                    }
                },
                
            }
        },
        {
            "$group": {
                "_id": {
                    "date": "$date",
                    "isRefund": "$isRefund"
                },
                "goods_number": {"$sum": "$goods_number"},
                "goods_amount": {"$sum": "$goods_amount"}
            }
        },
        {
            "$group": {
                "_id": "$_id.date",
                "data": {
                    "$push": {
                        "isRefund": "$_id.isRefund",
                        "goods_number": "$goods_number",
                        "goods_amount": "$goods_amount"
                    }
                },
                
            }
        },
        
        # {
        #     "$project": {
        #         "data": {
        #             "$arrayToObject": "$data"
        #         }
        #     }
        # }
    ])


def query_advertise_of_goods(coll_name: str, id: int, days: int):
    agg_ad_search = db[coll_name].aggregate(
        [
            {
                "$match": {
                    "goodsId": id,
                    "statDate": {"$gt": datetime.datetime.fromtimestamp(
                        time.time() - days * SECONDS_EACH_DAY)},
                }
            },
            {
                "$addFields": {
                    "date": {
                        "$dateToString": {
                            "date": "$statDate",
                            "format": "%Y-%m-%d"
                        }
                    }
                }
            },
            {
                "$group": {
                    "_id": "$date",
                    "impression": {"$sum": "$impression"},
                    "orderNum": {"$sum": "$orderNum"},
                    "gmv": {"$sum": "$gmv"},
                    "spend": {"$sum": "$spend"},
                    "click": {"$sum": "$click"}
                }
            },
            {
                "$addFields": {
                    "_ctr": {"$cond": [{"$eq": ["$impression", 0]}, 0, {"$divide": ["$click", "$impression"]}]},
                    "_cvr": {"$cond": [{"$eq": ["$click", 0]}, 0, {"$divide": ["$orderNum", "$click"]}]},
                    "_roi": {"$cond": [{"$eq": ["$spend", 0]}, 0, {"$divide": ["$gmv", "$spend"]}]},
                }
            }
        ]
    )
    return agg_ad_search


def query_detail_of_goods(id: int, with_sku_list: bool):
    return db[COLL_GOODS_LIST].find_one({"_id": id}, None if with_sku_list else {"sku_list": 0})


def query_comments_of_goods(id: int, days: int):
    return db[COLL_GOODS_COMMENTS_DETAIL].aggregate([
        {
            "$addFields": {
                "date": {
                    "$dateFromString": {
                        "dateString": "$statDate",
                        "format": "%Y-%m-%d"
                    },
                }
            }
        },
        {
            "$match": {
                "_id.goodsId": id,
                "date": {
                    "$gt": datetime.datetime.fromordinal(
                        (datetime.date.today() - datetime.timedelta(days=days)).toordinal())
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "mallId": 0,
                "updateTime": 0,
                "date": 0
            }
        }
    ])


@core_router.get('/query', summary='一次性获取某个商品的所有信息（日频）', response_model=BaseResponseModel)
def core_query_goods(
    id: int = Query(DEFAULT_GOODS_ID, description='商品ID'),
    days: int = Query(14, description='从今天零点起往前总计日数'),
    with_sku: bool = Query(True, description='获取SKU的交易细分数据'),
    with_refund: bool = Query(True, description="获取汇总、退款等相关数据"),
    with_advertise: bool = Query(True, description='获取多多推广、多多场景、放心推等推广数据'),
    with_goods_detail: bool = Query(True, description='获取商品明细数据'),
    with_goods_comments: bool = Query(True, description='获取商品评价数据'),
    opt_sku_long_table: bool = Query(False, description='获取SKU交易原数据，适合pandas后续处理'),
    opt_sku_list: bool = Query(False, description='获取每个商品的SKU列表数据'),
    # with_mall_info: bool = Query(True, description="获取销售该商品的店铺信息")
):
    result = dict()
    if with_sku:
        result['sku'] = list(query_sku_of_goods(id, days, opt_sku_long_table))
    
    if with_refund:
        result['refund'] = list(query_total_of_goods(id, days))
    
    if with_advertise:
        for coll_name in [COLL_AD_SEARCH, COLL_AD_SCENE, COLL_AD_FANGXIN]:
            result[coll_name] = list(query_advertise_of_goods(coll_name, id, days))
    
    # todo: 不完善，太多字段还需额外处理
    if with_goods_detail:
        result["goods_detail"] = query_detail_of_goods(id, opt_sku_list)
    
    if with_goods_comments:
        result['goods_comments'] = list(query_comments_of_goods(id, days))
    
    return {"result": result, "success": True, "msg": "提取成功"}
