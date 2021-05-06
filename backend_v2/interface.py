from datetime import datetime
from typing import TypedDict, Any


class PddResult(TypedDict):
    success: bool
    result: Any


class PddUserInfo(TypedDict):
    id: int
    username: str
    hasLogin: bool


class UserInfo(PddUserInfo):
    _id: int
    password: str
    cookie: str
    updateTime: datetime
