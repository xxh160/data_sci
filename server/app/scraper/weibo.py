import json
import re
import time
from datetime import datetime
from functools import partial
from queue import Queue

from lxml import etree

from app.util.news_util import NewsParser, ua
from app.util.str_util import str_list_process, str_process, remove_sign
from app.util.yaml_util import read_yaml


def search(date: datetime, keywords: str) -> list:
    tar_url = "https://s.weibo.com/weibo?q={0}&xsort=hot&suball=1&timescope=custom:{1}:{1}&Refer=g".format(keywords,
                                                                                                           date.date())
    news_manager = login()
    urls = find_urls(news_manager, tar_url, 1)
    res_queue = Queue()
    part = partial(get_one, news_parser=news_manager, res=res_queue)
    NewsParser.run(part, urls)
    news_manager.close()
    return list(res_queue.queue)


if __name__ == '__main__':
    search(datetime.now(), "yi")


def find_urls(news_parser, base_url, max_num) -> Queue:
    res = Queue()
    # html = news_parser.get_static(base_url)
    raw = news_parser.get_static_raw(base_url)
    html = etree.HTML(raw)
    cur_html = html
    while max_num >= 1:
        cur_urls = cur_html.xpath("//a[@action-type='fl_unfold']/@href")
        # res.extend(["https:" + cur_url for cur_url in cur_urls])
        for cur_url in cur_urls:
            res.put("https:" + cur_url)
        next_url = html.xpath("//a[@class='next']/@href")
        if len(next_url) == 0:
            break
        cur_html = news_parser.get_static("https://s.weibo.com" + next_url[0])
        max_num -= 1
        time.sleep(1)
    return res


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


def get_one(url: str, news_parser: NewsParser, res: Queue):
    try:
        topic = get_topic(news_parser, url)
        # time.sleep(2)
        # cur_time = get_time(news_parser, url)
        # time.sleep(2)
        comments = get_comments(news_parser, url)
        # time.sleep(2)
        res.put({"topic": topic, "comments": comments, "url": url})
    except Exception as e:
        print(e.args)
        pass
    time.sleep(1)


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
