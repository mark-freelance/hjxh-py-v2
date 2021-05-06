import os

PATH_ROOT = os.path.abspath(os.path.dirname(__file__))
PATH_API = os.path.join(PATH_ROOT, "backend_v1")
PATH_SIMULATE = os.path.join(PATH_ROOT, "simulate")

PATH_VERSION_FILE = os.path.join(PATH_ROOT, "../VERSION.txt")

DEFAULT_USERNAME = "乐和食品店:冯露"
DEFAULT_PASSWORD = "FL123456..."

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

EPS = 1e-6
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
URL_GET_PDD_USER_INFO = "https://yingxiao.pinduoduo.com/mms-gateway/user/info"