import os

# alias
import urllib.parse

EPS = 1e-6
SECONDS_EACH_DAY = 86400
MILLISECONDS_EACH_DAY = 86400000
MILLISECONDS_DELAY = 1000

# path
PATH_ROOT = os.path.abspath(os.path.dirname(__file__))
PATH_API = os.path.join(PATH_ROOT, "backend_v1")
PATH_SCRIPTS = os.path.join(PATH_ROOT, "scripts")
PATH_SCRIPT_GET_ANTI_CONTENT = os.path.join(PATH_SCRIPTS, 'getAntiContent.js')
PATH_SIMULATE = os.path.join(PATH_ROOT, "simulate")
PATH_VERSION_FILE = os.path.join(PATH_ROOT, "../VERSION.txt")
PATH_NODE = '/usr/local/bin/node'

# accounts
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
DEFAULT_USERNAME = "乐和食品店:冯露"
DEFAULT_PASSWORD = "FL123456..."
DEFAULT_MALL_ID = 506673970
DEFAULT_USER_ID = 93917892
DEFAULT_GOODS_ID = 221058511472

# url
URL_FETCH_USER_INFO = 'https://mms.pinduoduo.com/janus/api/new/userinfo'
# URL_FETCH_USER_INFO_REDUNDANT = "https://yingxiao.pinduoduo.com/mms-gateway/user/info"


# ad
KEY_AD_ID = '商品 ID'
AD_MAP = {
    "数据时间": 'target_date',
    '渠道': 'source',
    '流量': '点击量',
    '点击率': '点击率',
    '转化': '点击转化率',
    '投产': '投入产出比',
    '销量': '成交笔数',
    '成交额': '每笔成交金额',
    '花费': '千次曝光花费',
}

# mongodb config
MONGO_HOST = "nanchuan.site"
MONGO_PORT = 2708
MONGO_AUTHENTICATION_DATABASE = "hjxh-operate"
MONGO_DATABASE_NAME = "hjxh-operate"
MONGO_USERNAME = 'hjxh-operator'
MONGO_PASSWORD = "hjxh-operator"
username = urllib.parse.quote_plus(MONGO_USERNAME)
password = urllib.parse.quote_plus(MONGO_PASSWORD)
MONGO_URI = f'mongodb://{username}:{password}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DATABASE_NAME}?authSource={MONGO_AUTHENTICATION_DATABASE}'


# mongodb coll names
COLL_USERS = 'users'
COLL_ORDERS = "orders"
COLL_AD_SEARCH = "ad_search"
COLL_AD_SCENE = "ad_scene"
COLL_AD_FANGXIN = "ad_fangxin"
COLL_GOODS_LIST = "goods_list"
COLL_GOODS_DETAIL = "goods_detail"
COLL_GOODS_COMMENTS_LIST = "goods_comments_list"
COLL_GOODS_COMMENTS_DETAIL = "goods_comments_detail"
COLL_STATS = 'stats'
EXCLUDE_ORDER_STATUS_LIST = [
    '待支付',
    '已取消'
]