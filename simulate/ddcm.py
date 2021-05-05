import time

from simulate.config.const import TIME_DELAY, PATH_DDCM_COOKIES
from simulate.utils.driver import driver
from simulate.utils.driver_supports import get_cookie_dict
from simulate.utils.io import json_dump, json_load
from log import logger

if __name__ == '__main__':
    URL_DDCM_LOGIN = 'https://ddqbt.mobduos.com/#/member/login'
    DDCM_USERNAME = 18516271865
    DDCM_PASSWORD = 'Ss523659...'

    logger.info("正在访问登录页")
    driver.get(URL_DDCM_LOGIN)
    time.sleep(TIME_DELAY)
    driver.find_element_by_xpath('//input[@placeholder="手机号/账号"]').send_keys(DDCM_USERNAME)
    driver.find_element_by_xpath('//input[@placeholder="密码"]').send_keys(DDCM_PASSWORD)
    driver.find_element_by_class_name('login-button').click()

    logger.info("等待通过验证码")
    time.sleep(10)
    json_dump(get_cookie_dict(driver), PATH_DDCM_COOKIES)
    cookies = json_load(PATH_DDCM_COOKIES)

    logger.info("正在访问监控页")
    driver.get('https://ddqbt.mobduos.com/#/sku-monitor/monitor')

    url = 'https://ddqbt.mobduos.com/api/qbt/v1/sku-monitor/monitorGoodsSkuList'
    goodsId = '198465122449'
    params = {"goodsId": goodsId}

