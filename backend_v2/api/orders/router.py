from functools import partial

from fastapi import APIRouter, Depends

from utils.db_support import db_general_query
from database.client import db

api_orders = APIRouter(tags=['订单系统'], prefix='/orders')

coll_orders = db['orders']


@api_orders.get('/')
def get_orders(dep=Depends(partial(db_general_query, 'orders'))):
    return dep
