import json
import re
import time

from lxml import etree

from util.spiders.news_parser import NewsParser, ua1
from util.str_util import str_list_process, str_process, remove_sign


# def find_urls(news_parser, num):
#     result = []
#     for i in range(num):
#         all_urls = news_parser.get_dynamic_elements('//div[@class="box-result clearfix"]//a')
#         result.extend([cur_url.get_attribute("href") for cur_url in all_urls])
#         news_parser.get_dynamic_element('//table[@style="margin:0 auto;"]//a[@title="下一页"]').click()
#     return result

def find_urls(news_parser, base_url, max_num):
    res = []
    # html = news_parser.get_static(base_url)
    raw = news_parser.get_static_raw(base_url)
    html = etree.HTML(raw)
    cur_hcdtml = html
    while max_num >= 1:
        cur_urls = cur_html.xpath("//a[@action-type='fl_unfold']/@href")
        res.extend(["https:" + cur_url for cur_url in cur_urls])
        next_url = html.xpath("//a[@class='next']/@href")
        if len(next_url) == 0:
            break
        cur_html = news_parser.get_static("https://s.weibo.com" + next_url[0])
        max_num -= 1
        time.sleep(1)
    return set(res)


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


def get_one(news_parser: NewsParser, url: str, res: list):
    try:
        topic = get_topic(news_parser, url)
        # time.sleep(2)
        cur_time = get_time(news_parser, url)
        # time.sleep(2)
        comments = get_comments(news_parser, url)
        # time.sleep(2)
        res.extend([topic, cur_time, url, comments])
    except Exception as e:
        print(e.args)
        pass


def get_all():
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    news_manager = NewsParser("https://weibo.com/login.php", ua1)
    news_manager.login({'name': '18851863569',
                        'passwd': 'sci9scidatehhh14',
                        'login_name_xpath': "//input[@id='loginname']",
                        'passwd_xpath': "//input[@type='password']",
                        'submit_xpath': "//a[@suda-data='key=tblog_weibologin3&value=click_sign']"
                        })
    # news_manager.get_dynamic_element("//a[@node-type='searchSubmit']").click()
    # news_manager.get_dynamic_element("//input[@node-type='text']").send_keys("新冠疫情")
    # news_manager.get_dynamic_element("//button[@class='s-btn-b']").click()
    # news_manager.get_dynamic_element("//a[@node-type='advsearch']").click()

    urls = find_urls(news_manager,
                     "https://s.weibo.com/weibo/%25E7%25A5%259E%25E5%25A5%2587%25E5%25A5%25B3%25E4%25BE%25A01984%25E4%25B8%25AD%25E5%259B%25BD%25E9%25A6%2596%25E6%2598%25A0%25E7%25A4%25BC?q=%E6%96%B0%E5%86%A0%E7%96%AB%E6%83%85&xsort=hot&suball=1&timescope=custom:2020-02-01:2020-11-30&Refer=g"
                     , 1)
    last_res = []
    for url in urls:
        res = []
        get_one(news_manager, url, res)
        last_res.append(res)
    news_manager.close()
    return last_res


if __name__ == '__main__':
    final_res = get_all()
    for cur in final_res:
        print(cur[0], cur[1], cur[2])
        for comment in cur[3]:
            print(comment)
