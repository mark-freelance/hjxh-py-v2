import os
import re
import time

from selenium.webdriver.remote.webdriver import WebDriver

from log import logger
from simulate.config.const import PATH_DDBK_COOKIES, URL_DDBK_HOME, PATH_DATA, TIME_DELAY, URL_DDBK_LOGIN, \
    URL_DDBK_LOGOUT, DDBK_TARGET_TO_USE, DDBK_TARGET_LOGIN_VIA_ACCOUNT
from simulate.utils.accounts import accounts
from simulate.utils.driver import driver
from simulate.utils.driver_supports import get_cookie_dict, find_ele_with_text
from simulate.utils.io import json_dump, json_load


def auto_login(driver):
    if not hot_login(driver):
        visit_login(driver)
        kill_window(driver)
        start_login(driver)
        json_dump(get_cookie_dict(driver), PATH_DDBK_COOKIES)
    logger.info("登录成功")


def is_ddbk_login_success(driver):
    return re.search(r'\.com/home', driver.current_url)


def hot_login(driver: WebDriver) -> bool:
    logger.info("正在尝试热启动，首先初始化访问首页")
    driver.get(URL_DDBK_HOME)
    cookie_list = json_load(os.path.join(PATH_DATA, "ddbk-COOKIE-list.json"))
    for cookie in cookie_list:
        driver.add_cookie({"name": cookie["name"], "value": cookie["value"]})
    logger.info("Cookie装载完毕，重新访问，请等待……")
    driver.get(URL_DDBK_HOME)
    time.sleep(TIME_DELAY * 3)
    if is_ddbk_login_success(driver):
        logger.info("热启动成功，当前网址：" + driver.current_url)
        json_dump(get_cookie_dict(driver), PATH_DDBK_COOKIES)
        return True
    else:
        logger.info("热启动失败，尝试重新登录，可能需要管路员手机验证码，当前网址：" + driver.current_url)
        return False


def visit_login(driver: WebDriver):
    driver.get(URL_DDBK_LOGIN)


def logout(driver: WebDriver):
    driver.get(URL_DDBK_LOGOUT)


def kill_window(driver: WebDriver):
    """
    去除弹窗
    :param driver:
    :return:
    """
    if DDBK_TARGET_TO_USE not in driver.page_source:
        logger.info(f"未检测到（{DDBK_TARGET_TO_USE}）选项")
    else:
        logger.info(f"被PDD检测到正在使用Driver，正在确认（{DDBK_TARGET_TO_USE}）选项")
        
        ele_confirm_webdriver = find_ele_with_text(driver, DDBK_TARGET_TO_USE)
        if not ele_confirm_webdriver:
            logger.warning(f"未能成功定位到{DDBK_TARGET_TO_USE}")
        else:
            logger.info(f"已成功定位到{DDBK_TARGET_TO_USE}，正在点击……")
            ele_confirm_webdriver.click()
            logger.info(f"已点击{DDBK_TARGET_TO_USE}")
            assert DDBK_TARGET_TO_USE not in driver.page_source, f"{DDBK_TARGET_TO_USE}还是存在，可能有误"


def start_login(driver: WebDriver):
    """
    用账户登录
    :param driver:
    :return:
    """
    ele_login_via_account = find_ele_with_text(driver, DDBK_TARGET_LOGIN_VIA_ACCOUNT)
    assert ele_login_via_account is not None, f"未能检测到{DDBK_TARGET_LOGIN_VIA_ACCOUNT}按钮"
    ele_login_via_account.click()
    
    username = accounts["pdd_backend"]["username"]
    password = accounts["pdd_backend"]["password"]
    driver.find_element_by_id("usernameId").send_keys(username)
    driver.find_element_by_id("passwordId").send_keys(password)
    
    TARGET_TO_LOGIN = "登录"
    ele_login_btn = find_ele_with_text(driver, TARGET_TO_LOGIN)
    assert ele_login_btn is not None, f"未检测到{TARGET_TO_LOGIN}按钮"
    logger.info(f"正在点击{TARGET_TO_LOGIN}按钮")
    ele_login_btn.click()
    
    #  进入后台
    time.sleep(TIME_DELAY * 3)
    assert is_ddbk_login_success(driver), "未能成功登录"
    logger.info("已成功跳转到首页")
    
    
if __name__ == '__main__':
    auto_login(driver)
    logger.info("正在退出浏览器")
    driver.quit()
