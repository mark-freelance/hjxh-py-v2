from fastapi import APIRouter

from api.ad.fangxin.router import api_ad_fangxin
from api.ad.scene.router import api_ad_scene
from api.ad.search.router import api_ad_search

api_ad = APIRouter(tags=['推广系统'], prefix='/ad')

api_ad.include_router(api_ad_search)
api_ad.include_router(api_ad_scene)
api_ad.include_router(api_ad_fangxin)
