from fastapi import APIRouter

from database.client import db

api_detail = APIRouter(prefix='/detail')

coll_detail = db['goods_detail']


@api_detail.get('/')
def get_detail(limit: int = 20):
    return list(coll_detail.find({}).limit(limit))
