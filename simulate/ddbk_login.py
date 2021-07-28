import atexit
import json
import os
import re
import signal
import time

import sys
sys.path.insert(0, '/Users/mark/projects/HJXH/hjxh-py')

from log import logger
from simulate.config.const import PATH_DDBK_COOKIES, URL_DDBK_HOME, TIME_DELAY, URL_DDBK_LOGIN, \
    URL_DDBK_LOGOUT, DDBK_TARGET_TO_USE, DDBK_TARGET_LOGIN_VIA_ACCOUNT, TARGET_TO_LOGIN, COOKIE_JAR_DIR, COOKIE_STR_DIR
from simulate.utils.accounts import accounts
from simulate.utils.driver import driver
from simulate.utils.driver_supports import get_cookie_dict, find_ele_with_text
from simulate.utils.io import json_dump, json_load


class MyDriver:
    def __init__(self, username, cookie_format="jar"):
        self._username = username
        self._cookie_format = cookie_format
        self._driver = driver
        
        self._cookie_jar_path: str = os.path.join(COOKIE_JAR_DIR, self._username + ".json")
        self._cookie_str_path: str = os.path.join(COOKIE_STR_DIR, self._username + '.txt')
        
        atexit.register(self._driver.quit)
        signal.signal(signal.SIGINT, self.cleanup)
        logger.info('registered cleanup')
        
    def cleanup(self, code, frame):
        """
        
        @param code:
        @param frame: 程序快照，存储着函数栈、线程、全局变量等
        @return:
        """
        logger.info('called destroy')
        logger.info(code)
        logger.info(frame)
        self._driver.quit()
    
    def auto_login(self):
        if not self.hot_login():
            self.visit_login()
            self.kill_window()
            self.start_login()
            json_dump(get_cookie_dict(self._driver), PATH_DDBK_COOKIES)
        logger.info("登录成功")
    
    def is_ddbk_login_success(self):
        return re.search(r'\.com/home', self._driver.current_url)
    
    def _load_cookie_str(self):
        with open(os.path.join(COOKIE_STR_DIR, self._username + '.txt'), 'r') as f:
            cookie_str = f.read().splitlines()[-1]
            for cookie in cookie_str.split(";"):
                if cookie:
                    name, value = cookie.split("=", 1)
                    self._driver.add_cookie({"name": name, "value": value})
    
    def _load_cookie_jar(self):
        cookie_jar = json_load(os.path.join(COOKIE_JAR_DIR, self._username + '.json'))
        for cookie in cookie_jar:
            self._driver.add_cookie({"name": cookie["name"], "value": cookie["value"]})
    
    def load_cookie(self):
        if self._cookie_format == 'str':
            logger.info("loading str type of cookie")
            self._load_cookie_str()
        else:
            logger.info('loading jar type of cookie')
            self._load_cookie_jar()
        logger.info("loaded cookie")
    
    def _get_cookie_jar(self):
        return self._driver.get_cookies()
    
    def _get_cookie_str(self):
        return ";".join(["=".join([item["name"], item['value']]) for item in self._driver.get_cookies()])
    
    def _dump_cookie_jar(self):
        json.dump(self._get_cookie_jar(), open(self._cookie_jar_path, 'w'), indent=2, ensure_ascii=False)
    
    def _dump_cookie_str(self):
        with open(self._cookie_str_path, "w") as f:
            f.write(self._get_cookie_str())
    
    def dump_cookie(self):
        if self._cookie_format == 'str':
            self._dump_cookie_jar()
        else:
            self._dump_cookie_str()
        logger.info("dumped cookie into: " + self._cookie_jar_path)
    
    def hot_login(self) -> bool:
        logger.info("正在尝试热启动，首先初始化访问首页")
        self._driver.get(URL_DDBK_HOME)
        self.load_cookie()
        
        logger.info('重新加载首页')
        self._driver.get(URL_DDBK_HOME)
        time.sleep(TIME_DELAY * 3)
        if self.is_ddbk_login_success():
            logger.info("热启动成功，当前网址：" + self._driver.current_url)
            json_dump(get_cookie_dict(self._driver), PATH_DDBK_COOKIES)
            return True
        else:
            logger.info("热启动失败，尝试重新登录，可能需要管理员手机验证码，当前网址：" + self._driver.current_url)
            return False
    
    def visit_login(self):
        self._driver.get(URL_DDBK_LOGIN)
    
    def logout(self):
        self._driver.get(URL_DDBK_LOGOUT)
    
    def kill_window(self):
        """
        去除弹窗
        :param _driver:
        :return:
        """
        if DDBK_TARGET_TO_USE not in self._driver.page_source:
            logger.info(f"未检测到（{DDBK_TARGET_TO_USE}）选项")
        else:
            logger.info(f"被PDD检测到正在使用Driver，正在确认（{DDBK_TARGET_TO_USE}）选项")
            
            ele_confirm_webdriver = find_ele_with_text(self._driver, DDBK_TARGET_TO_USE)
            if not ele_confirm_webdriver:
                logger.warning(f"未能成功定位到{DDBK_TARGET_TO_USE}")
            else:
                logger.info(f"已成功定位到{DDBK_TARGET_TO_USE}，正在点击……")
                ele_confirm_webdriver.click()
                logger.info(f"已点击{DDBK_TARGET_TO_USE}")
                assert DDBK_TARGET_TO_USE not in self._driver.page_source, f"{DDBK_TARGET_TO_USE}还是存在，可能有误"
    
    def start_login(self) -> bool:
        """
        用账户登录
        :param _driver:
        :return:
        """
        ele_login_via_account = find_ele_with_text(self._driver, DDBK_TARGET_LOGIN_VIA_ACCOUNT)
        assert ele_login_via_account is not None, f"未能检测到{DDBK_TARGET_LOGIN_VIA_ACCOUNT}按钮"
        ele_login_via_account.click()
        
        username = accounts["pdd_backend"]["username"]
        password = accounts["pdd_backend"]["password"]
        self._driver.find_element_by_id("usernameId").send_keys(username)
        self._driver.find_element_by_id("passwordId").send_keys(password)
        
        ele_login_btn = find_ele_with_text(self._driver, TARGET_TO_LOGIN)
        assert ele_login_btn is not None, f"未检测到{TARGET_TO_LOGIN}按钮"
        logger.info(f"正在点击{TARGET_TO_LOGIN}按钮")
        ele_login_btn.click()
        
        # todo: 智能判断wait
        #  进入后台
        time.sleep(TIME_DELAY * 3)
        return self.is_ddbk_login_success()


if __name__ == '__main__':
    
    my_driver = MyDriver("乐和食品店:冯露", cookie_format='jar')
    my_driver.auto_login()
    logger.inf("正在退出浏览器")
