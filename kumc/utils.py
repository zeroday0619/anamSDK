from datetime import datetime


def get_now_yymmdd():
    now = datetime.now()
    return int(now.strftime('%Y%m%d'))