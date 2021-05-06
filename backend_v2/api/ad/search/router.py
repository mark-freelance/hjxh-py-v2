from fastapi import APIRouter

from database.client import db

coll_ad_search = db['ad_search']

api_ad_search = APIRouter(prefix='/search')


@api_ad_search.get('/')
def get_ad_search(limit: int = 20):
    return list(coll_ad_search.find({}).limit(limit))
