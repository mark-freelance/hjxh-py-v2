from fastapi import APIRouter

from api.goods.comments.router import api_comments
from api.goods.detail.router import api_detail

api_goods = APIRouter(prefix='/goods', tags=['商品系统'])

api_goods.include_router(api_detail)
api_goods.include_router(api_comments)
