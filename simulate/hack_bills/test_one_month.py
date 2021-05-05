from datetime import datetime

from simulate.hack_bills.core import get_bills_of_day
from log import logger

if __name__ == '__main__':
    for day in range(23, 0, -1):
        logger.info(f">>> crawling day: {day}")
        date_start = int(datetime(2021, 4, day, 0, 0).timestamp())
        get_bills_of_day(date_start)
