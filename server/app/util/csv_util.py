import os

from pandas import DataFrame


def write_helper(path: str, name: str, df: DataFrame):
    path = os.path.join(path, name)
    if os.path.exists(path):
        df.to_csv(path, index=False, mode="a", header=False, sep=",")
    else:
        df.to_csv(path, index=False, mode="w", header=False, sep=",")


def add_postfix(postfix: str, path: str):
    if path[-1] is not '/':
        path = path + '/'
    file_list = os.listdir(path)
    for cur in file_list:
        old_name = os.path.join(path, cur)
        new_name = os.path.join(path, cur + postfix)
        os.rename(old_name, new_name)


def add_prefix(prefix: str, path: str):
    if path[-1] is not '/':
        path = path + '/'
    file_list = os.listdir(path)
    for cur in file_list:
        old_name = os.path.join(path, cur)
        new_name = os.path.join(path, prefix + cur)
        os.rename(old_name, new_name)


if __name__ == '__main__':
    add_postfix(".csv", "../scraper/store/bilibili/", )
    add_prefix("bilibili_", "../scraper/store/bilibili/")
