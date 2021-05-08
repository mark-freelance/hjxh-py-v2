from datetime import datetime
from functools import partial
from typing import TypedDict
import re

from fastapi import APIRouter, Depends, HTTPException, Query, Form
from pydantic import BaseModel

from database.mongodb_client import db
from database.mongodb_query import db_query
from interface import UserInfo
from utils.verify_user import verify_cookie_strict, preprocess_cookie

users_router = APIRouter(tags=['账号系统'], prefix='/users')

coll_users = db['users']


class UserAjaxResult(TypedDict, total=False):
    success: bool
    result: UserInfo
    msg: str


def find_user(username: str = Query(..., description='拼多多店铺,用户名')) -> UserAjaxResult:
    user = coll_users.find_one({"username": username})
    if not user:
        return {
            "success": False,
            "msg": 'not found user of name: ' + username
        }
    else:
        return {
            "success": True,
            "result": user
        }


@users_router.get('/', summary='获取所有用户信息')
def get_users(dep=Depends(partial(db_query, 'users'))):
    return dep


@users_router.put('/verify_cookie', summary='验证cookie是否有效')
def verify_cookie(cookie: str = Form(..., description="拼多多店铺cookie")) -> UserAjaxResult:
    cookie = preprocess_cookie(cookie)
    try:
        return {
            "success": True,
            "result": {
                **verify_cookie_strict(cookie),
                "cookie": cookie
            }
        }
    except Exception as e:
        return {
            "success": False,
            "msg": e.__str__()
        }


@users_router.put('/verify_cookie_of_user', summary='验证某个用户的cookie是否有效')
def verify_cookie_of_user(user=Depends(find_user)) -> UserAjaxResult:
    return verify_cookie(user['_cookie'])


@users_router.put('/update_cookie_of_user', summary='更新某个用户的cookie信息')
def update_cookie_of_user(aj1: UserAjaxResult = Depends(find_user),
                          aj2: UserAjaxResult = Depends(verify_cookie)) -> UserAjaxResult:
    if not aj1['success']:
        return aj1
    
    if not aj2['success']:
        return aj2
    
    u1 = aj1['result']['username']
    u2 = aj2['result']['username']
    if u1 != u2:
        return {
            "success": False,
            "msg": f'username mismatch, `{u1}` != `{u2}`'
        }
    
    res = coll_users.find_one_and_update({'username': u1}, {"$set": aj2['result']})
    return {
        "success": True,
        "result": res,
        "msg": "已更新~"
    }


class CreateUserModel(BaseModel):
    username: str = Form(..., description='拼多多店铺用户名')
    password: str = Form(..., description='拼多多店铺渺茫')
    cookie: str = Form(..., description='拼多多店铺cookie')


@users_router.post('/add', summary='新增一个用户')
def add_user(
    user: CreateUserModel
) -> UserAjaxResult:
    if coll_users.find_one({"username": user.username}):
        return {"success": False, "msg": f'user of name `{user.username}` has existed!'}
    res = verify_cookie(user.cookie)
    if not res['success']:
        return res
    
    user_info: UserInfo = res['result']
    if user_info['username'] != user.username:
        raise HTTPException(400, f'username mismatch, `{user.username}` != `{user_info["username"]}`')
    user_info['password'] = user.password
    user_info['updateTime'] = datetime.now()
    user_info['_id'] = user_info['id']
    coll_users.insert_one(user_info)
    return {
        "success": True,
        "result": coll_users.find_one({"_id": user_info["_id"]})
    }
