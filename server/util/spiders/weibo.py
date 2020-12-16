import json
import re

from lxml import etree

from util.decorator import str_list_process
from util.news_parser import NewsParser, ua1


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
    cur_html = html
    while max_num >= 1:
        cur_urls = cur_html.xpath("//a[@action-type='fl_unfold']/@href")
        res.extend(["https:" + cur_url for cur_url in cur_urls])
        next = html.xpath("//a[@class='next']/@href")
        if len(next) == 0:
            break
        cur_html = news_parser.get_static("https://s.weibo.com" + next[0])
        max_num -= 1
    return res


def get_topic(news_parser):
    pass


def get_time(news_parser):
    pass


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
        cur_res = []
        comments = get_comments(news_parser, url)
        cur_res.append(comments)
        res.append(cur_res)
    except Exception as e:
        print(e.args)
        pass


def get_all():
    news_manager = NewsParser("https://weibo.com/login.php", ua1)
    news_manager.login({'name': '<your-login-name>',
                        'passwd': '<your-password>',
                        'login_name_xpath': "//input[@id='loginname']",
                        'passwd_xpath': "//input[@type='password']",
                        'submit_xpath': "//a[@suda-data='key=tblog_weibologin3&value=click_sign']"
                        })
    # news_manager.get_dynamic_element("//a[@node-type='searchSubmit']").click()
    # news_manager.get_dynamic_element("//input[@node-type='text']").send_keys("新冠疫情")
    # news_manager.get_dynamic_element("//button[@class='s-btn-b']").click()
    # news_manager.get_dynamic_element("//a[@node-type='advsearch']").click()

    urls = find_urls(news_manager,
                     "https://s.weibo.com/weibo?q=%E6%96%B0%E5%86%A0%E7%96%AB%E6%83%85&xsort=hot&suball=1&timescope=custom:2020-01-31:2020-12-01&Refer=g",
                     1)
    last_res = []
    # return NewsParser.run(get_one, urls)
    for url in urls:
        res = []
        get_one(news_manager, url, res)
        last_res.append(res)
    return last_res


if __name__ == '__main__':
    final_res = get_all()
    for cur in final_res:
        for comment in cur[-1]:
            print(comment)
