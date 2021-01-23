import json
import re
import time
from datetime import datetime, date, timedelta

from lxml import etree
from pandas import DataFrame, Series

from app.util.news_util import NewsParser, ua
from app.util.str_util import str_list_process, str_process, remove_sign
from app.util.yaml_util import read_yaml


def login():
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    news_manager = NewsParser("https://weibo.com/login.php", ua)
    # 相对路径是魔鬼啊
    log = read_yaml("../../resource/log_config.yml")
    news_manager.login({'name': log["weibo"]["name"],
                        'passwd': log["weibo"]["password"],
                        'login_name_xpath': "//input[@id='loginname']",
                        'passwd_xpath': "//input[@type='password']",
                        'submit_xpath': "//a[@suda-data='key=tblog_weibologin3&value=click_sign']"
                        })
    return news_manager


def find_urls(news_parser, base_url, max_num) -> list:
    res = []
    # html = news_parser.get_static(base_url)
    raw = news_parser.get_static_raw(base_url)
    html = etree.HTML(raw)
    cur_html = html
    while max_num >= 1:
        cur_urls = cur_html.xpath("//a[@action-type='fl_unfold']/@href")
        # res.extend(["https:" + cur_url for cur_url in cur_urls])
        for cur_url in cur_urls:
            res.append("https:" + cur_url)
        next_url = html.xpath("//a[@class='next']/@href")
        if len(next_url) == 0:
            break
        cur_html = news_parser.get_static("https://s.weibo.com" + next_url[0])
        max_num -= 1
        time.sleep(1)
    print("total: " + str(len(res)))
    return list(set(res))


@str_process
def get_topic(news_parser, url):
    static_raw = news_parser.get_static_raw(url)
    static = etree.HTML(static_raw)
    return static.xpath('//head//title/text()')[0]


def get_time(news_parser, url):
    static_raw = news_parser.get_static_raw(url)
    static = etree.HTML(static_raw)
    cur_list = static.xpath('//script/text()')
    res_a = []
    for script in cur_list:
        script_cur = script[3000:7000]
        if "feed_list_item_date" in script_cur:
            res_a = re.findall('.*(<a.*?feed_list_item_date.*?/a>).*', script_cur)
            break
    res_a = remove_sign(res_a[0], '\\')
    next_html = etree.HTML(res_a)
    res_time = next_html.xpath("//a/@title")
    return res_time[0].strip()


@str_list_process
def get_comments(news_parser, url):
    static = news_parser.get_static(url)
    mid_list = static.xpath("//script/text()")
    mid = []
    for cur_mid in mid_list:
        if "act=" in cur_mid:
            mid = re.findall(r'.*act=(\d+).*', cur_mid)
            break
    mid = eval(mid[0])
    html = news_parser.get_static_raw(
        "https://weibo.com/aj/v6/comment/big?ajwvr=6&id={}&from=singleWeiBo&__rnd=1608146907945".format(mid),
        encoding='Unicode')
    json_ins = json.loads(html)
    comments_html = etree.HTML(json_ins['data']['html'])
    comments = comments_html.xpath("//div[@class='list_li S_line1 clearfix']//div[@class='WB_text']/text()")
    return comments


def get_one(url: str, news_parser: NewsParser):
    res = []
    try:
        res = all_comments(news_parser, url)
    except Exception as e:
        print(e.args)
    return res


# @str_list_process
def all_comments(news_parser: NewsParser, url) -> list:
    news_parser.reset(url)
    # scroll = "var q=document.getElementById('id').scrollTop=10000"
    for i in range(4):
        news_parser.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(3)
    news_parser.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    for i in range(5):
        try:
            news_parser.click("//a[@action-type='click_more_comment']/span[@class='more_txt']")
        except Exception as e:
            print(e.args)
            break
        time.sleep(1)
    comments_nodes = news_parser.get_dynamic_elements(
        "//div[@class='list_li S_line1 clearfix']//div[@class='WB_text']")
    comments = [cur.text for cur in comments_nodes if "等人" not in cur.text]
    print(comments)
    return comments


def get_all(tar_date: date, keywords: str, news_manager: NewsParser) -> Series:
    begin = time.time()
    tar_url = "https://s.weibo.com/weibo?q={0}&xsort=hot&suball=1&timescope=custom:{1}:{1}&Refer=g".format(keywords,
                                                                                                           tar_date)
    urls = find_urls(news_manager, tar_url, 3)
    res = []
    for url in urls:
        try:
            res.extend(all_comments(news_manager, url))
        except Exception:
            pass
    end = time.time()
    print("time: " + str(end - begin))
    print({str(date): res})
    return Series(res)


def run(begin: datetime, end: datetime, keywords: str):
    news_manager = login()
    begin_time = begin.date()
    end_time = end.date()
    while begin_time <= end_time:
        print(begin_time)
        cur_res = get_all(begin_time, keywords, news_manager)
        df = DataFrame({begin_time: cur_res})
        df.to_csv("./store/weibo/" + "weibo_" + str(begin_time) + ".csv")
        begin_time += timedelta(days=1)
    news_manager.close()


if __name__ == '__main__':
    # search(datetime(2020, 12, 31), datetime(2020, 12, 31), "新冠疫情")
    print("1:2".split(":")[1])
    tmp = ["1", "2", "1", 2]
    print(list(set(tmp)))
