import csv

from typing import List

csv_head1 = ["topic", "time", "con/m", "url"]
csv_head2 = ["comments"]
csv_head3 = ["content"]
csv_head4 = ["weibo", "bili", "people", "south"]


def full_path(name: str, path: str) -> str:
    postfix = ".csv"
    if postfix not in name:
        name += postfix
    return path + name


def create_csv(name: str, path: str, headers: list):
    final_path = full_path(name, path)
    with open(final_path, 'w', newline='') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(headers)


def write_csv(name: str, path: str, headers: list, content: List[dict]):
    final_path = full_path(name, path)
    with open(final_path, 'a', newline='') as f:
        csv_write = csv.DictWriter(f, headers)
        csv_write.writerows(content)


def read_csv(name: str, path: str, headers: list) -> list:
    final_path = full_path(name, path)
    res = []
    with open(final_path, 'r')as f:
        csv_read = csv.DictReader(f, headers)
        for row in csv_read:
            res.update(row)
    return res


def rewrite_csv(name: str, path: str, headers: list, content: List[dict]):
    create_csv(name, path, headers)
    write_csv(name, path, headers, content)


if __name__ == '__main__':
    create_csv("test", "..\\scraper\\store\\", csv_head1)
    write_csv("test", "..\\scraper\\store\\", csv_head1, [{"topic": "a", "time": "b", "con/m": "content1", "url": "d"},
                                                          {"topic": "a", "time": "b", "con/m": "comment1", "url": "d"}])
    read_csv("test", "..\\scraper\\store\\", csv_head1)
