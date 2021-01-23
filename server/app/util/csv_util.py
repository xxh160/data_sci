import os

from pandas import DataFrame


def write_helper(path: str, name: str, df: DataFrame):
    path = os.path.join(path, name)
    if os.path.exists(path):
        df.to_csv(path, index=False, mode="a", header=False, sep=",")
    else:
        df.to_csv(path, index=False, mode="w", header=False, sep=",")
