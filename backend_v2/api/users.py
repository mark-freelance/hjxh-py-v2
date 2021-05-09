import time
from functools import partial

from fastapi import APIRouter, Depends, Query, Form
from pydantic import BaseModel

from api.core import BaseResponseModel
from database.mongodb_client import db
from database.mongodb_query import db_query
from interface import UserInfo
from utils.verify_user import verify_cookie_strict, preprocess_cookie

users_router = APIRouter(tags=['账号系统'], prefix='/users')

coll_users = db['users']


@users_router.get('/find_user', summary='查找账号是否存在', response_model=BaseResponseModel)
def find_user(username: str = Query(..., description='拼多多店铺,用户名')) -> (UserInfo or None):
    user_info = coll_users.find_one({"username": username})
    if user_info:
        return {
            "success": True,
            "result": user_info
        }
    else:
        return {
            "msg": "not found username of " + username
        }


@users_router.get('/', summary='获取所有用户信息')
def get_users(dep=Depends(partial(db_query, 'users'))):
    return dep


@users_router.put('/verify_cookie', summary='验证cookie是否有效', response_model=BaseResponseModel)
def verify_cookie(cookie: str = Form(..., description="拼多多店铺cookie")):
    cookie = preprocess_cookie(cookie)
    try:
        user_info = verify_cookie_strict(cookie)
    except Exception as e:
        return {
            "msg": e.__str__()
        }
    else:
        return {
            "success": True,
            "result": {
                **user_info,
                "cookie": cookie
            }
        }


@users_router.put('/verify_cookie_of_user', summary='验证某个用户的cookie是否有效', response_model=BaseResponseModel)
def verify_cookie_of_user(user_result=Depends(find_user)):
    """
    这个函数应该会调用多次，所以应该轻量
    
    @param user_result:
    @return:
    """
    if not user_result.get('success'):
        return user_result
    user_1 = user_result['result']
    res = verify_cookie(user_1['cookie'])
    success = res.get('success', False)
    coll_users.update_one(
        {"_id": user_1['_id']},
        {"$set": {"verifiedTime": time.time(), "verifiedStatus": success}},
    )
    if success:
        return {
            "success": True,
            "msg": "验证通过"
        }
    else:
        return {
            "msg": "验证失败"
        }


@users_router.put('/update_cookie_of_user', summary='更新某个用户的cookie信息', response_model=BaseResponseModel)
def update_cookie_of_user(aj1=Depends(find_user),
                          aj2=Depends(verify_cookie)):
    """
    这个函数用于更新用户的cookie，应该返回足量的信息
    
    @param aj1:
    @param aj2:
    @return:
    """
    if not aj1.get('success'):
        return aj1
    
    if not aj2.get('success'):
        return aj2
    
    u1 = aj1['result']['username']
    u2 = aj2['result']['username']
    if u1 != u2:
        return {
            "msg": f'username mismatch, `{u1}` != `{u2}`'
        }
    user = coll_users.find_one_and_update(
        {"username": aj2['result']['username']},
        {"$set": {"verifiedTime": time.time(), "verifiedStatus": True, **aj2['result']}},
        return_document=True
    )
    
    return {"success": True, "result": user, "msg": '更新成功'}


class CreateUserModel(BaseModel):
    username: str = Form(..., description='拼多多店铺用户名')
    password: str = Form(..., description='拼多多店铺渺茫')
    cookie: str = Form(..., description='拼多多店铺cookie')


@users_router.post('/add', summary='新增一个用户', response_model=BaseResponseModel)
def add_user(user: CreateUserModel):
    """
    新增用户的设计机制同上
    
    @param user:
    @return:
    """
    if coll_users.find_one({"username": user.username}):
        return {"msg": f'user_result of name `{user.username}` has existed!'}
    res = verify_cookie(user.cookie)
    if not res.get('success'):
        return res
    
    user_info: UserInfo = res.get('result', '')
    if not user_info:
        return {"msg": "程序异常"}
    if user_info['username'] != user.username:
        return {"msg": f'username mismatch, `{user.username}` != `{user_info["username"]}`'}
    user_info['password'] = user.password
    user_info['verifiedTime'] = time.time()
    user_info['verifiedStatus'] = True
    user_info['_id'] = user_info['id']
    coll_users.insert_one(user_info)
    return {
        "success": True,
        "result": coll_users.find_one({"_id": user_info["_id"]})
    }
