from _datetime import datetime

from app.scraper.operation import store

if __name__ == '__main__':
    store(datetime(2020, 4, 7), datetime(2020, 5, 1), "新冠疫情")
