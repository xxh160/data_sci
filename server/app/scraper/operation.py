from datetime import datetime

from app.scraper import weibo
from app.util.csv_util import read_num, write_normal, rewrite_nums, write_comments


def save_weibo(date: datetime, keywords: str):
    res = weibo.search(date, keywords)
    df = read_num("cur_num", "./store/")
    nums = df.loc[0]
    comment_name = "comments_" + str(date.date()) + "_" + str(nums[-1])
    weibo_name = "weibo" + str(date.date()) + "_" + str(nums[0])
    data = []
    for cur in res:
        topic = cur["topic"]
        url = cur["url"]
        data.append([topic, date.date(), comment_name, url])
        comments = cur["comments"]
        write_comments(comment_name, "./store/comment/", comments)
        nums[-1] += 1
        comment_name = "comments_" + str(date.date()) + "_" + str(nums[-1])
    write_normal(weibo_name, "./store/informal/", data)
    nums[0] += 1
    rewrite_nums("cur_num", "./store/", nums)


if __name__ == '__main__':
    save_weibo(datetime.now(), "新冠疫情")
