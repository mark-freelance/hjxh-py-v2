from datetime import datetime

from simulate.hack_bills.core import get_bills_of_day

if __name__ == '__main__':
    """
    测试一天
    """
    date_start = int(datetime(2021, 4, 23, 0, 0).timestamp())
    get_bills_of_day(date_start)
