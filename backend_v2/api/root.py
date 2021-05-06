from fastapi import APIRouter

from .ad.router import api_ad
from .goods.router import api_goods
from .orders.router import api_orders
from .users.router import api_users

api_root = APIRouter(prefix='/api/v2')

api_root.include_router(api_orders)
api_root.include_router(api_ad)
api_root.include_router(api_goods)
api_root.include_router(api_users)
