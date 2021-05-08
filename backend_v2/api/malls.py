from fastapi import APIRouter

from database.mongodb_client import db
from database.mongodb_query import AjaxResult
from settings import COLL_USERS, COLL_GOODS_LIST

malls_router = APIRouter(prefix='/malls', tags=['店铺系统'])


@malls_router.get('/', summary='获取所有店铺')
def get_malls() -> AjaxResult:
    cursor = db[COLL_USERS].find({})
    return {
        "success": True,
        "result": {
            "total": cursor.count(),
            "items": list(cursor)
        }
    }


@malls_router.get('/goods', summary='获取某店铺下的所有商品', tags=['商品系统'])
def get_goods_from_mall(mall_id: int) -> AjaxResult:
    cursor = db[COLL_GOODS_LIST].find({"mallId": mall_id}, {"sku_list": 0})
    return {
        "success": True,
        "result": {
            "total": cursor.count(),
            "items": list(cursor)
        }
    }


