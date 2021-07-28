import datetime
from functools import partial

import pandas as pd
from fastapi import APIRouter, Depends

from database.mongodb_client import db
from database.mongodb_query import AjaxResult, db_query
from settings import COLL_AD_FANGXIN, COLL_AD_SEARCH, COLL_AD_SCENE

ad_router = APIRouter(tags=['推广系统'], prefix='/ad')


@ad_router.get('/search', summary='获取所有商品的多多搜索数据')
def get_ad_search(dep: AjaxResult = Depends(partial(db_query, COLL_AD_SEARCH))):
    return dep


@ad_router.get('/scene', summary='获取所有商品的多多场景数据')
def get_ad_scene(dep: AjaxResult = Depends(partial(db_query, COLL_AD_SCENE))):
    return dep


@ad_router.get('/fangxin', summary='获取所有商品的放心推数据')
def get_ad_fangxin(dep: AjaxResult = Depends(partial(db_query, COLL_AD_FANGXIN))):
    return dep


@ad_router.get('/all', summary='一次性获取某商品某天的所有推广数据')
def get_ad_all(goods_id: int = 221058511472, days: int = 7) -> AjaxResult:
    AD_COLUMNS = ['click', 'impression', 'orderNum', 'gmv', 'spend', '_ctr', '_cvr', '_roi']

    def calc_ad_item(coll_name: str, goods_id: int, days: int):
        # print(coll_name, goods_id, date)
        start_time = datetime.datetime.fromordinal(
            (datetime.date.today() - datetime.timedelta(days=days)).toordinal())
        return db[coll_name].aggregate([
            {
                "$match": {
                    "goodsId": goods_id,
                    "statDate": {"$gte": start_time}
                }
            },
            {
                "$group": {
                    "_id": "$statDate",
                    "click": {"$sum": "$click"},  # 点击量
                    "impression": {"$sum": "$impression"},  # 曝光量
                    "orderNum": {"$sum": "$orderNum"},  # 成交笔数
                    "gmv": {"$sum": "$gmv"},  # 交易额
                    "spend": {"$sum": "$spend"}  # 花费
                }
            },
            {
                "$addFields": {
                    "_ctr": {  # 点击率 = 点击量 / 曝光量
                        "$cond": [{"$eq": ["$impression", 0]}, 0, {"$divide": ["$click", "$impression"]}]
                    },
                    "_cvr": {  # 转化率 = 成交笔数 / 点击量
                        # "$divide": ['$orderNum', "$click"]
                        "$cond": [{"$eq": ["$click", 0]}, 0, {"$divide": ["$orderNum", "$click"]}]
                    },
                    "_roi": {  # 投产 = 交易额 / 花费
                        # '$divide': ['$gmv', '$spend']
                        "$cond": [{"$eq": ["$spend", 0]}, 0, {"$divide": ["$gmv", "$spend"]}]
                    }
                }
            },
            {
                "$addFields": {
                    "date": {
                        "$dateToString": {
                            "date": "$_id",
                            "format": "%Y-%m-%d",
                            "timezone": "+08"
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0
                }
            }
        ])
    
    def handle(name):
        df = pd.DataFrame(calc_ad_item(name, goods_id, days), columns=['date'] + AD_COLUMNS)
        df.set_index('date', inplace=True)
        df.rename(columns=dict((i, i + '_' + name) for i in AD_COLUMNS), inplace=True)
        return df
    
    df = pd.concat(map(handle, [COLL_AD_SEARCH, COLL_AD_SCENE, COLL_AD_FANGXIN]), axis=1)
    
    items = df.sort_index(ascending=False).fillna(0).reset_index().to_dict(orient='records')
    
    return {
        "success": True,
        "result": {
            "items": items,
            "total": len(items)
        }
    }
