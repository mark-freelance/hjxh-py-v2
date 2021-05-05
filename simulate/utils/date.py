from datetime import datetime, date, timedelta


def get_yesterday():
    yesterday = date.today() - timedelta(days=1)
    return datetime(*yesterday.timetuple()[:3])
