import os
from datetime import datetime, timedelta

import pandas as pd

from app.scraper import weibo, bilibili, south
from app.util.csv_util import write_helper


def sort_raw_by_date():
    dir_path = "./raw"
    all_files = os.listdir(dir_path)
    # df = pd.read_csv(os.path.join(dir_path, "1传33！大连本轮疫情出现超级传播.csv"), sep=',')
    # begin = datetime.strptime(df.head(1)["日期"].values[0], "%Y-%m-%d").date()
    # end = datetime.strptime(df.tail(1)["日期"].values[0], "%Y-%m-%d").date()
    for cur_file in all_files:
        df = pd.read_csv(os.path.join(dir_path, cur_file), sep=',')
        begin = datetime.strptime(df.head(1)["日期"].values[0], "%Y-%m-%d").date()
        end = datetime.strptime(df.tail(1)["日期"].values[0], "%Y-%m-%d").date()
        while begin <= end:
            cur_df = df[df["日期"] == str(begin)]
            write_helper("./store/bilibili", "bilibili_" + str(begin) + ".csv", cur_df)
            print(cur_df)
            begin += timedelta(days=1)


def store(begin: datetime, end: datetime, keywords: str):
    bilibili.bilibili()
    weibo.run(begin, end, keywords)
    south.run(begin.date(), end.date(), keywords)
    sort_raw_by_date()


if __name__ == '__main__':
    # print({str(datetime(2020, 2, 1).date()): 1})
    # store(datetime(2020, 5, 2), datetime(2020, 6, 1), "新冠疫情")
    sort_raw_by_date()
