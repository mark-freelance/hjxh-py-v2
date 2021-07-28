import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from log import logger
from settings import DEFAULT_USER_AGENT
from simulate.config.const import DDBK_TARGET_LOGIN_VIA_ACCOUNT, TIME_DELAY, TARGET_TO_LOGIN, DRIVER_PATH, \
    TIME_IMPLICIT_WAIT, URL_DDBK_LOGIN
from simulate.ddbk_login import is_ddbk_login_success
from simulate.utils.driver_supports import find_ele_with_text


class PddSimulator(WebDriver):
    def __init__(self, username: str, password: str):
        options = Options()
        options.add_argument("user-agent=" + DEFAULT_USER_AGENT)
        super().__init__(DRIVER_PATH, options=options)
        self.maximize_window()
        ws = self.get_window_size()
        w = ws["width"]
        h = ws["height"]
        self.set_window_rect(w / 2, 0, w / 2, h)
        self.implicitly_wait(TIME_IMPLICIT_WAIT)  # seconds
        # cdp 全称是：Chrome Devtools-Protocol，通过 addScriptToEvaluateOnNewDocument() 方法可以在页面还未加载之前，运行一段脚本。
        self.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """Object.defineProperty(navigator, "webdriver", {get: () => undefined})"""
        })
        
        self.username = username
        self.password = password
    
    def start_login(self):
        """
        用账户登录
        """
        self.get(URL_DDBK_LOGIN)
        time.sleep(TIME_DELAY * 2)
        
        ele_login_via_account = find_ele_with_text(self, DDBK_TARGET_LOGIN_VIA_ACCOUNT)
        assert ele_login_via_account is not None, f"未能检测到{DDBK_TARGET_LOGIN_VIA_ACCOUNT}按钮"
        ele_login_via_account.click()
        
        self.find_element_by_id("usernameId").send_keys(self.username)
        self.find_element_by_id("passwordId").send_keys(self.password)
        
        ele_login_btn = find_ele_with_text(self, TARGET_TO_LOGIN)
        assert ele_login_btn is not None, f"未检测到{TARGET_TO_LOGIN}按钮"
        logger.info(f"正在点击{TARGET_TO_LOGIN}按钮")
        ele_login_btn.click()
        
        #  进入后台
        time.sleep(TIME_DELAY * 3)
        assert is_ddbk_login_success(self), "未能成功登录"
        logger.info("已成功跳转到首页")


if __name__ == '__main__':
    username = '乐和食品店:冯露'
    password = 'FL123456...'
    pdd_simulator = PddSimulator(username, password)
    pdd_simulator.start_login()
