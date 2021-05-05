from datetime import datetime

from simulate.hack_bills.core import get_bills_of_day
from log import logger

'''
# follow
from simulate.config.const import SECONDS_PER_DAY
d = int(datetime(2021, 4, 25).timestamp())
while get_bills_of_day(d):
    logger.info("=== 开始爬取下一日 ===")
    d -= SECONDS_PER_DAY
'''

if __name__ == '__main__':
    
    logger.info("started fetching bills")
    get_bills_of_day(int(datetime(2021, 4, 25).timestamp()))
    logger.info("finished fetching bills")
