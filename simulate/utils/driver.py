# from seleniumwire import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from simulate.config.const import TIME_IMPLICIT_WAIT, PATH_DRIVER

"""
1. 反爬检测当前浏览器窗口下的 window.navigator 对象是否包含 webdriver 这个属性。
    在正常使用浏览器的情况下，这个属性是 undefined，而使用 selenium 时为 true。
    因此可以通过执行脚本从而绕过该检测
2. 但是 ChromeDriver 79.0.3945.36 版本修改了非无头模式下排除 “启用自动化” 时 window.navigator.webdriver 是未定义的问题.
    要想正常使用，需要把 Chrome 回滚 79 之前的版本，并找到对应的 ChromeDriver 版本，这样才可以
"""

options = Options()

#  add ua
from simulate.utils.driver_supports import get_random_UA
options.add_argument("user-agent=" + get_random_UA())

#  不可以无头，会导致找不到登录按钮
# options.add_argument("headless")

# 隐藏 正在受到自动软件的控制 这几个字
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# options.add_argument("--disable-blink-features")
# options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(PATH_DRIVER, options=options)
driver.maximize_window()
ws = driver.get_window_size()
w = ws["width"]
h = ws["height"]
driver.set_window_rect(w / 2, 0, w / 2, h)
driver.implicitly_wait(TIME_IMPLICIT_WAIT)  # seconds

"""
cdp 全称是：Chrome Devtools-Protocol
通过 addScriptToEvaluateOnNewDocument() 方法可以在页面还未加载之前，运行一段脚本。
"""
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """Object.defineProperty(navigator, "webdriver", {get: () => undefined})"""
})
