from app.util.spiders import observer, tian_ya, weibo


def connect_to_mysql():
    pass


def save():
    observer_res = observer.get_all()
    tian_ya_res = tian_ya.get_all()
    weibo_res = weibo.get_all()


if __name__ == '__main__':
    save()
