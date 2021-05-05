from datetime import datetime

from fastapi import APIRouter

from db.ad import db_fetch_ads_of_id

api_ad = APIRouter(prefix='/ad', tags=['推广数据'])


@api_ad.get('/', summary='获得最近的推广数据')
def get_ad():
    return [db_fetch_ads_of_id('221058511472', datetime(2021, 4, 25))]

