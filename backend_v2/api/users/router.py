from datetime import datetime
from functools import partial

from fastapi import APIRouter, Depends, HTTPException, Body, Query
from pydantic import BaseModel

from database.client import db
from interface import UserInfo
from utils.db_support import db_general_query
from utils.user_support.verify_user import core_verify_cookie

api_users = APIRouter(tags=['账号系统'], prefix='/users')

coll_users = db['users']


def find_user(username: str = Query(..., description='拼多多店铺用户名')) -> UserInfo:
    user = coll_users.find_one({"username": username})
    if not user:
        raise HTTPException(400, 'not found user of name: ' + username)
    else:
        return user


@api_users.get('/')
def get_users(dep=Depends(partial(db_general_query, 'users'))):
    return dep


@api_users.get('/verify_cookie')
def verify_cookie(cookie: str = Query(..., description="拼多多店铺cookie")) -> UserInfo:
    try:
        return core_verify_cookie(cookie)
    except Exception as e:
        raise HTTPException(400, e.__str__())


@api_users.get('/verify_cookie_of_user')
def verify_cookie_of_user(user=Depends(find_user)) -> UserInfo:
    try:
        return verify_cookie(user['cookie'])
    except Exception as e:
        raise HTTPException(400, e.__str__())


@api_users.put('/update_cookie_of_user')
def update_cookie_of_user(user_item=Depends(find_user), user_info=Depends(verify_cookie)) -> UserInfo:
    u1 = user_item['username']
    u2 = user_info['username']
    if u1 != u2:
        raise HTTPException(400, f'username mismatch, `{u1}` != `{u2}`')
    else:
        return coll_users.find_one_and_update({'username': u1}, {"$set": {'cookie': user_info['cookie']}})


class CreateUserModel(BaseModel):
    username: str = Query(..., description='拼多多店铺用户名')
    password: str = Query(..., description='拼多多店铺渺茫')
    cookie: str = Query(..., description='拼多多店铺cookie')


@api_users.post('/add')
def add_user(
    user: CreateUserModel
) -> UserInfo:
    if coll_users.find_one(user.username):
        raise HTTPException(400, f'user of name `{user.username}` has existed!')
    user_info: UserInfo = verify_cookie(user.cookie)
    if user_info['username'] != user.username:
        raise HTTPException(400, f'username mismatch, `{user.username}` != `{user_info["username"]}`')
    user_info['password'] = user.password
    user_info['updateTime'] = datetime.now()
    user_info['_id'] = user_info['id']
    coll_users.insert_one(user_info)
    return coll_users.find_one({"_id": user_info["_id"]})
