from fastapi import APIRouter

from database.client import db

coll_ad_scene = db['ad_scene']

api_ad_scene = APIRouter(prefix='/scene')


@api_ad_scene.get('/')
def get_ad_scene(limit: int = 20):
    return list(coll_ad_scene.find({}).limit(limit))

