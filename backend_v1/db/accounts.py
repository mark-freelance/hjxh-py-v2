import time

from database.mongodb_client import db
from api.models.accounts import AccountCategory, AccountStatus, Account
from log import logger

coll_accounts = db["accounts"]


def db_add_account(username, password, category: AccountCategory, note=None):
    account: Account = Account(username=username, password=password, category=category, note=note,
                               created_time=int(time.time()), status=AccountStatus.NotVerified)
    account_item = account.dict()
    logger.info(f"added account: {account_item}")
    return coll_accounts.insert_one(account_item)


def db_fetch_accounts(category: AccountCategory = None):
    if not category:
        return list(coll_accounts.find())
    else:
        return list(coll_accounts.find({"category": category.value}))
