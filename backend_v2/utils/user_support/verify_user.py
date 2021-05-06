import os
import subprocess

import requests

from interface import PddResult, UserInfo
from log import logger
from settings import UA, URL_GET_PDD_USER_INFO

SCRIPT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'getAntiContent.js')


def core_verify_cookie(cookie: str) -> UserInfo:
    """
    最重要的两个字段是 _nano_fp 和 SUB_PASS_ID
    """
    assert cookie, 'cookie不能为空！'
    cookie = [i for i in cookie.split() if i][-1]
    
    # logger.info({"script_path": SCRIPT_PATH, "cookie": cookie})
    
    try:
        # anti_content = subprocess.check_output(['node', SCRIPT_PATH, cookie],
        #                                        encoding='utf-8').strip()
        
        anti_content = subprocess.Popen(['node', SCRIPT_PATH, cookie], stdout=subprocess.PIPE,
                                        encoding='utf-8').stdout.read().strip()
        
        logger.info({"anti-content": anti_content})
        
    except Exception as e:
        logger.error('anti-content算法调用失败：', e.__str__())
        raise e
    
    data = {'crawlerInfo': anti_content, 'mallId': None}
    
    headers = {'anti-content': anti_content, 'user-agent': UA, 'COOKIE': cookie}
    
    res: PddResult = requests.post(URL_GET_PDD_USER_INFO, data=data, headers=headers).json()
    
    if not res.get('success'):  # 失败之时没有success字段
        raise ValueError('cookie无效：', res)
    if not res['result']['hasLogin']:
        raise ValueError('该账号尚未登录：', res)
    
    user_info = res['result']
    user_info['cookie'] = cookie
    return user_info


def core_verify_username_cookie(username: str, cookie: str):
    userinfo = core_verify_cookie(cookie)
    username2 = userinfo['username']
    if username != username2:
        raise ValueError(f'username不匹配，输入的username: {username}, cookie对应的username: {username2}')


def core_verify_user(username: str, password: str, cookie: str) -> dict:
    logger.warning('todo: verification of password support')
    """
    todo: 校验password
    """
    try:
        core_verify_username_cookie(username, cookie)
    except Exception as e:
        logger.error(e)
        logger.info('校验失败！')
        return {
            'success': False,
            'msg': str(e)
        }
    else:
        logger.info('校验通过！')
        return {
            'success': True
        }
