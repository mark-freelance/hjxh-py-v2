import os
from database.mongodb_client import db

SECONDS_PER_DAY = 86400 # 24 * 60 * 60

TIME_IMPLICIT_WAIT = 3
TIME_DELAY = 1
PAGE_SIZE = 50

URL_DDBK_LOGIN = 'https://mms.pinduoduo.com/login'
URL_DDBK_LOGOUT = "https://mms.pinduoduo.com/janus/api/logout"
URL_DDBK_HOME = 'https://mms.pinduoduo.com/home/'
URL_DDBK_CHECK_BILLS = 'https://mms.pinduoduo.com/mangkhut/mms/recentOrderList'

DDBK_TARGET_TO_USE = "已安装去使用"
DDBK_TARGET_LOGIN_VIA_ACCOUNT = "账户登录"
DDBK_TARGET_KEYS_BASE = ['曝光量', '成交笔数', '交易额', '花费']
DDBK_TARGET_KEYS_EXTEND = DDBK_TARGET_KEYS_BASE + ["点击量"]

PATH_SIMULATE = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PATH_ACCOUNTS = os.path.join(PATH_SIMULATE, "config/accounts.yaml")
PATH_DATA = os.path.join(PATH_SIMULATE, "data")
PATH_DDBK_COOKIES = os.path.join(PATH_DATA, "ddbk-cookies.json")
PATH_DDCM_COOKIES = os.path.join(PATH_DATA, "ddcm-cookies.json")

PATH_DRIVER = os.path.join(os.path.dirname(__file__), "../execute-drivers/chromedriver-v90")

coll_bills = db['bills']
coll_detail = db['detail']
coll_promote = db['promote']

DEFAULT_HEADER = {
    "Content-Type": "application/json;charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
}

TARGET_EXIT_INTRO_WINDOW = '退出介绍'


TARGET_PROMOTE_1_HEAD = '//*[@id="__next"]/div/div[2]/div/div/div/div/div[6]/div[5]/div[2]/div/div/div/div[1]/table/thead/tr'
TARGET_PROMOTE_1_ROWS = '//*[@id="__next"]/div/div[2]/div/div/div/div/div[6]/div[5]/div[2]/div/div/div/div[1]/table/tbody/tr'
TARGET_PROMOTE_2_HEAD = '//*[@id="__next"]/div/div[2]/div/div/div/div/div[4]/div[5]/div[2]/div/div/div/div[1]/table/thead/tr'
TARGET_PROMOTE_2_ROWS = '//*[@id="__next"]/div/div[2]/div/div/div/div/div[4]/div[5]/div[2]/div/div/div/div[1]/table/tbody/tr'
TARGET_PROMOTE_3_HEAR = '//*[@id="__next"]/div/div[2]/div/div/div/div/div[7]/div/div/div/div[1]/table/thead/tr'
TARGET_PROMOTE_3_ROWS = '//*[@id="__next"]/div/div[2]/div/div/div/div/div[7]/div/div/div/div[1]/table/tbody/tr'
XPATH_TABLE_HEADER = '//*[@data-testid="beast-core-table-middle-thead"]//th'
XPATH_TABLE_CONTENT_ROWS = '//*[@data-testid="beast-core-table-middle-tbody"]//tr'


