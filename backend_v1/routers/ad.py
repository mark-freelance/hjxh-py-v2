from datetime import datetime

from fastapi import APIRouter

from database.ad import db_fetch_ads_of_id

router_ad = APIRouter(prefix='/ad', tags=['推广数据'])


@router_ad.get('/', summary='获得最近的推广数据')
def get_ad():
    return [db_fetch_ads_of_id('221058511472', datetime(2021, 4, 25))]

