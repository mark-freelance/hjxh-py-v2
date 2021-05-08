from functools import partial

from fastapi import APIRouter, Depends

from database.mongodb_query import AjaxResult, db_query
from settings import COLL_GOODS_LIST, COLL_GOODS_DETAIL, COLL_GOODS_COMMENTS_LIST

goods_router = APIRouter(prefix='/goods', tags=['商品系统'])


@goods_router.get('/list', summary='获取所有商品列表信息')
def get_goods_list(dep: AjaxResult = Depends(partial(db_query, COLL_GOODS_LIST))):
    return dep


@goods_router.get('/detail', summary='获取所有商品详情信息')
def get_goods_detail(dep: AjaxResult = Depends(partial(db_query, COLL_GOODS_DETAIL))):
    return dep


@goods_router.get('/comments', summary='获取所有商品评论信息')
def get_goods_detail(dep: AjaxResult = Depends(partial(db_query, COLL_GOODS_COMMENTS_LIST))):
    return dep
