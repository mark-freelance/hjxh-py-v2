from fastapi import APIRouter

from api.ad import ad_router
from api.goods import goods_router
from api.malls import malls_router
from api.orders import orders_router
from api.users import users_router

root_router = APIRouter(prefix='/api/v2')

root_router.include_router(orders_router)
root_router.include_router(goods_router)
root_router.include_router(ad_router)
root_router.include_router(malls_router)
root_router.include_router(users_router)
