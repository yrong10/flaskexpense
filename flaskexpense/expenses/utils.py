from datetime import datetime


def todate(s):
    return datetime.strptime(s, "%Y-%m-%d")
