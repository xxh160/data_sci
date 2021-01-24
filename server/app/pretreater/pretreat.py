import datetime
import os
from _datetime import timedelta

import numpy as np


def read(file):
    f = open(file, "r", encoding="utf-8")
    content = f.read()
    lines = content.split("\n")
    f.close()
    try:
        while lines[len(lines) - 1].isspace() or lines[len(lines) - 1] == "":
            lines.pop(len(lines) - 1)
    except:
        print(file)
    return lines


def write(file, lines):
    f = open(file, "w", encoding="utf-8")
    for line in lines:
        f.write(line + "\n")
    f.close()
    return


def norm(datalist):  # 计算数据的均值和标准差
    x = np.array(datalist)
    mu = np.mean(x)
    sigma = np.std(x)
    list = []
    list.append(mu)
    list.append(sigma)
    return list


def pretreatment(resoucedir, targetdir, begin_time, end_time):
    files = os.listdir(resoucedir)
    resfrom = ""
    if "bilibili" in resoucedir:
        resfrom = "bilibili_"
    if "weibo" in resoucedir:
        resfrom = "weibo_"
    if "south" in resoucedir:
        resfrom = "south_"
    list = []
    begin = begin_time
    while begin <= end_time:
        realpath = resoucedir + resfrom + str(begin) + ".csv"
        lines = read(realpath)
        list.append(len(lines))
        begin += timedelta(days=1)
        pass
    mu_and_sig = norm(list)
    begin = begin_time
    if resfrom == "south_":
        mu_and_sig[0] = 0
    while begin <= end_time:
        realpath = resoucedir + resfrom + str(begin) + ".csv"
        lines = read(realpath)
        if len(lines) > mu_and_sig[0] - 0.5 * mu_and_sig[1] and len(lines) > 1:
            write(targetdir + resfrom + str(begin) + ".csv", lines)
            pass
        begin += timedelta(days=1)
        pass
    pass


if __name__ == "__main__":
    pretreatment("../scraper/store/weibo/", "./store/weibo/",
                 datetime.date(2019, 12, 31), datetime.date(2020, 1, 22))
    pretreatment("../scraper/store/weibo/", "./store/weibo/",
                 datetime.date(2020, 1, 23), datetime.date(2020, 2, 7))
    pretreatment("../scraper/store/weibo/", "./store/weibo/",
                 datetime.date(2020, 2, 8), datetime.date(2020, 3, 9))
    pretreatment("../scraper/store/weibo/", "./store/weibo/",
                 datetime.date(2020, 3, 10), datetime.date(2020, 6, 1))
    pretreatment("../scraper/store/bilibili/", "./store/bilibili/",
                 datetime.date(2020, 2, 9), datetime.date(2020, 3, 9))
    pretreatment("../scraper/store/bilibili/", "./store/bilibili/",
                 datetime.date(2020, 3, 10), datetime.date(2020, 6, 29))
    # pretreater("../scraper/store/bilibili/", "./store/bilibili/",
    #              datetime.date(2020, 6, 16), datetime.date(2020, 9, 30))
    # pretreater("../scraper/store/bilibili/", "./store/bilibili/",
    #              datetime.date(2020, 10, 1), datetime.date(2021, 1, 20))
    # pretreater("../scraper/store/south/", "./store/south/",
    #              datetime.date(2019, 12, 31), datetime.date(2020, 6, 15))
