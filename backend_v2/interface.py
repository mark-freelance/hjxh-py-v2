from datetime import datetime
from typing import TypedDict, Any, Union


class PddResult(TypedDict):
    success: bool
    result: Any


class PddUserInfo(TypedDict):
    id: int
    username: str
    hasLogin: bool


class UserInfo(PddUserInfo):
    _id: int
    userId: int
    password: str
    cookie: str
    verifiedTime: Union[int, float]
    verifiedStatus: bool
