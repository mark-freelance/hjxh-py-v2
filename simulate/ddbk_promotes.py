import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver

from database.mongodb_client import db
from log import logger
from simulate.config.const import TIME_DELAY, TARGET_PROMOTE_1_HEAD, TARGET_PROMOTE_1_ROWS, TARGET_PROMOTE_2_HEAD, \
    TARGET_PROMOTE_2_ROWS, TARGET_PROMOTE_3_HEAR, TARGET_PROMOTE_3_ROWS, TARGET_EXIT_INTRO_WINDOW, XPATH_TABLE_HEADER, \
    XPATH_TABLE_CONTENT_ROWS
from simulate.ddbk_login import auto_login
from simulate.utils.date import get_yesterday
from simulate.utils.driver import driver
from simulate.utils.driver_supports import find_ele_with_text, scroll_to_bottom

coll_promote = db['promote']
coll_promote_fangxin = db['promote_fangxin']


def parse_table(driver: WebDriver, source: str, extend_key=None, drop_tail=False):
    items = []
    keys = [e.text for e in driver.find_elements_by_xpath(XPATH_TABLE_HEADER)]
    for row in driver.find_elements_by_xpath(XPATH_TABLE_CONTENT_ROWS)[:-1 if drop_tail else None]:
        values = [td.text for td in row.find_elements_by_tag_name("td")]
        assert len(keys) == len(values)
        item = dict((i, j) for i, j in zip(keys, values))
        if extend_key:
            extend_str = item.pop(extend_key)
            item.update(dict(ij.split("：") for ij in extend_str.splitlines() if len(ij.split("：")) == 2))
        item["update_time"] = time.time()
        item['source'] = source
        item['target_date'] = get_yesterday()
        items.append(item)
    logger.info(f"表格解析完毕，数据维度为：({len(items)} x {len(keys)})")
    return items


def parse_promote(driver, target_head, target_rows, source, first_in=True):
    """
    这个函数用于解析推广页的表格数据
    最重要的是定位表格元素、判断列数（是否包含目标字段）
    以及三种场景的数据还是有差异（放心推，没有checkbox）
    """
    logger.info("正在解析当前promote页")
    
    if first_in:
        # 设置标题列，有三个齿轮，第一个是设置标题列，第二个无法点击（没找到），第三个是数据列
        logger.info("正在更改标题列信息")
        driver.find_elements_by_xpath('//*[@data-testid="beast-core-icon-gear"]')[2].click()
        ele_check_cols = driver.find_element_by_class_name('ant-drawer-body').find_elements_by_xpath(
            './/*[@data-testid="beast-core-icon-check"]')
        assert ele_check_cols.__len__() > 0, "未检测到可以点击的列标题项"
        for ele_check_col in ele_check_cols:
            if "active" not in ele_check_col.get_attribute("class"):
                ele_check_col.click()
        find_ele_with_text(driver, "确认").click()
        logger.info("已经选定所有标题列")
        time.sleep(TIME_DELAY)
        
        # 切换每页个数
        scroll_to_bottom(driver)
        driver.find_element_by_xpath('//*[@data-testid="beast-core-select-header"]').click()
        driver.find_element_by_xpath('//li/span[text()="50"]').click()
        scroll_to_bottom(driver)
        time.sleep(TIME_DELAY * 2)
    
    # 解析数据
    coll_promote.insert_many(parse_table(driver, extend_key='推广单元', source=source, drop_tail=True))
    
    # 下一页
    try:
        ele_next = driver.find_element_by_xpath('//li[@data-testid="beast-core-pagination-next"]')
        if 'disabled' not in ele_next.get_attribute("class"):
            ele_next.click()
            time.sleep(TIME_DELAY)
            parse_promote(driver, target_head, target_rows, source, first_in=False)
        else:
            logger.info("已爬取完本页")
    except NoSuchElementException:
        logger.info("已爬取完本页")


def parse_fangxin_promote(driver, target_head, target_rows, first_in=True):
    """
    这个函数用于解析推广页的表格数据
    最重要的是定位表格元素、判断列数（是否包含目标字段）
    以及三种场景的数据还是有差异（放心推，没有checkbox）
    """
    logger.info("正在解析当前promote页")
    # 切换每页个数
    scroll_to_bottom(driver)
    if first_in:
        driver.find_element_by_xpath('//*[@data-testid="beast-core-select-header"]').click()
        driver.find_element_by_xpath('//li/span[text()="50"]').click()
        time.sleep(TIME_DELAY * 2)
    
    # 解析数据
    coll_promote.insert_many(parse_table(driver, extend_key='商品', source="放心推", drop_tail=False))
    
    # 下一页
    try:
        scroll_to_bottom(driver)
        ele_next = driver.find_element_by_xpath('//li[@data-testid="beast-core-pagination-next"]')
        if 'disabled' not in ele_next.get_attribute("class"):
            ele_next.click()
            time.sleep(TIME_DELAY)
            parse_fangxin_promote(driver, target_head, target_rows, first_in=False)
        else:
            logger.info("已爬取完本页")
    except NoSuchElementException:
        logger.info("已爬取完本页")


def close_desc_window(driver):
    time.sleep(TIME_DELAY)
    if TARGET_EXIT_INTRO_WINDOW in driver.page_source:
        find_ele_with_text(driver, TARGET_EXIT_INTRO_WINDOW).click()
        assert TARGET_EXIT_INTRO_WINDOW not in driver.page_source, f"未能成功关闭弹窗{TARGET_EXIT_INTRO_WINDOW}"
    time.sleep(TIME_DELAY)


def fetch_ddss(driver: WebDriver):
    """
    多多搜索
    :param driver:
    :return:
    """
    logger.info("正在切换到多多搜索")
    driver.get('https://yingxiao.pinduoduo.com/marketing/main/center/search/list')
    time.sleep(TIME_DELAY * 3)
    logger.info("正在切换到昨天")
    find_ele_with_text(driver, '昨天').click()
    logger.info("正在切换到推广单元")
    time.sleep(TIME_DELAY)
    find_ele_with_text(driver, "推广单元").click()
    time.sleep(TIME_DELAY)
    parse_promote(driver, TARGET_PROMOTE_1_HEAD, TARGET_PROMOTE_1_ROWS, source="多多搜索")


def fetch_ddcj(driver: WebDriver):
    """
    多多场景
    :param driver:
    :return:
    """
    logger.info("正在切换到多多场景")
    driver.get('https://yingxiao.pinduoduo.com/marketing/main/center/scene/list')
    time.sleep(TIME_DELAY * 3)
    logger.info("正在切换到昨天")
    find_ele_with_text(driver, "昨天").click()
    time.sleep(TIME_DELAY)
    logger.info("正在切换到推广单元")
    find_ele_with_text(driver, "推广单元").click()
    time.sleep(TIME_DELAY)
    parse_promote(driver, TARGET_PROMOTE_2_HEAD, TARGET_PROMOTE_2_ROWS, source="多多场景")


def fetch_ddfxt(driver: WebDriver):
    """
    放心推
    """
    logger.info("正在切换到放心推")
    driver.get('https://yingxiao.pinduoduo.com/marketing/main/center/cpa/list')
    logger.info("正在切换到昨天")
    time.sleep(TIME_DELAY)
    find_ele_with_text(driver, "昨天").click()
    parse_fangxin_promote(driver, TARGET_PROMOTE_3_HEAR, TARGET_PROMOTE_3_ROWS)


def fetch_detail(driver: WebDriver):
    logger.info("正在访问商品详情页面")
    driver.get("https://mms.pinduoduo.com/sycm/goods_effect/detail")
    logger.info("勾选所有项")
    for ele_check in driver.find_elements_by_xpath('//*[@data-testid="beast-core-icon-check"]'):
        if 'active' not in ele_check.get_attribute('class'):
            ele_check.click()
    logger.info("解析页面")
    db['detail'].insert_many(parse_table(driver, source="商品详情"))


def fetch_comments(driver: WebDriver):
    logger.info("正在访问评价数据")
    driver.get('https://mms.pinduoduo.com/sycm/goods_quality/comment')
    scroll_to_bottom(driver)
    db['comments'].insert_many(parse_table(driver, source="商品评价"))


def fetch_promotes(driver):
    logger.info("started fetching promotes")
    fetch_ddss(driver)
    fetch_ddcj(driver)
    fetch_ddfxt(driver)
    # fetch_detail(_driver)
    # fetch_comments(_driver)
    logger.info("finished fetching promotes")


if __name__ == '__main__':
    auto_login(driver)
    fetch_promotes(driver)
    # _driver.quit()
