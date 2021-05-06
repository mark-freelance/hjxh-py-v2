from typing import List

from fastapi import APIRouter, Form

from database.accounts import db_fetch_accounts, db_add_account
from ..models.accounts import AccountCategory, Account
from ..models.base import MongoOutModel

api_accounts = APIRouter(prefix="/accounts", tags=["账号"])


class AccountOut(Account, MongoOutModel):
    pass


@api_accounts.get("/", response_model=List[AccountOut])
def get_accounts(category: AccountCategory = None):
    return db_fetch_accounts(category=category)


@api_accounts.post("/add")
def add_account(
    username: str = Form(..., description="店铺用户名"),
    password: str = Form(..., description="店铺密码"),
    category: AccountCategory = Form(..., description='渠道，目前支持<多多官方>和<多多参谋>两种'),
    note: str = Form(None, description='备注')
):
    db_add_account(username, password, category, note)
