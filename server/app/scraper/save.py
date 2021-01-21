from datetime import datetime

from app.scraper import weibo


def save_weibo(date: datetime, keywords: str):
    res = weibo.search(date, keywords)
    for cur in res:
        comments = cur["comments"]
        topic = cur["topic"]
        url = cur["topic"]
    pass


if __name__ == '__main__':
    save_weibo(datetime.now(), "1")
