from fastapi import APIRouter

from api.routers.accounts import api_accounts
from api.routers.ad import api_ad
from api.routers.bills import api_bills
from api.routers.pr import api_pr

api_root = APIRouter(prefix='/api/v1')

api_root.include_router(api_bills)
api_root.include_router(api_ad)
api_root.include_router(api_accounts)
api_root.include_router(api_pr)

