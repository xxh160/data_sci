import os

import pandas as pd
from pandas import DataFrame


def _full_path(name: str, path: str) -> str:
    postfix = ".csv"
    if postfix not in name:
        name += postfix
    return path + name


def _write_helper(final_path: str, df: DataFrame):
    if os.path.exists(final_path):
        df.to_csv(final_path, index=False, mode="a", header=False, sep=",")
    else:
        df.to_csv(final_path, index=False, mode="w", header=False, sep=",")


def read_normal(name: str, path: str) -> DataFrame:
    final_path = _full_path(name, path)
    res = pd.read_csv(final_path, header=None, names=["topic", "date", "content", "url"], sep=",")
    return res


def read_comments(name: str, path: str) -> DataFrame:
    final_path = _full_path(name, path)
    res = pd.read_csv(final_path, header=None, names=["comments"], sep=",")
    return res


def read_num(name: str, path: str) -> DataFrame:
    final_path = _full_path(name, path)
    res = pd.read_csv(final_path, header=None, names=["weibo", "bili", "people", "south", "comments"], sep=",")
    return res


def write_normal(name: str, path: str, data: list):
    final_path = _full_path(name, path)
    df = pd.DataFrame(data, columns=["topic", "date", "content", "url"])
    _write_helper(final_path, df)


def write_comments(name: str, path: str, data: list):
    final_path = _full_path(name, path)
    df = pd.DataFrame(data, columns=["comments"])
    _write_helper(final_path, df)


def write_nums(name: str, path: str, data: list):
    final_path = _full_path(name, path)
    df = pd.DataFrame([data], columns=["weibo", "bili", "people", "south", "comments"])
    _write_helper(final_path, df)


def rewrite_nums(name: str, path: str, data: list):
    final_path = _full_path(name, path)
    df = pd.DataFrame([data], columns=["weibo", "bili", "people", "south", "comments"])
    df.to_csv(final_path, index=False, mode="w", header=False, sep=",")


if __name__ == '__main__':
    print(read_num("test", "../scraper/store/"))
    rewrite_nums("test", "../scraper/store/", ["a", "b", "c", "d", "e"])
