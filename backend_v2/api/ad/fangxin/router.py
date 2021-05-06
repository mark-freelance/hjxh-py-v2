from fastapi import APIRouter

from database.client import db

coll_ad_fangxin = db['ad_fangxin']

api_ad_fangxin = APIRouter(prefix='/fangxin')


@api_ad_fangxin.get('/')
def get_ad_fangxin(limit: int = 20):
    return list(coll_ad_fangxin.find({}).limit(limit))

