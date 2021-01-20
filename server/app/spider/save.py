import datetime

import pymysql

from app.spider import observer, weibo
from app.spider import tian_ya


def connect_to_mysql():
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='123456',
        db='data_sci',
        charset='utf8mb4',
    )
    return connection


def save(begin: datetime, end: datetime, key: str):
    observer_res = observer.get_all()
    tian_ya_res = tian_ya.get_all()
    weibo_res = weibo.get_all()
    connection = connect_to_mysql()


if __name__ == '__main__':
    save()
