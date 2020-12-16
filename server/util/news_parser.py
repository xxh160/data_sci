import time
from threading import Thread

import requests
from lxml import etree
from selenium import webdriver

ua1 = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 ' \
      'Safari/537.36 '


def parse_cookies(cookie_str):
    res = {}
    for cookie in cookie_str.split(";"):
        key, value = cookie.split("=")
        res[key] = value
    return res


class NewsParser:
    def __init__(self, url, user_agent):
        """url最好是顶级域名"""
        self._url = url
        self._driver = None
        self._cookies = {}
        self._headers = {'User-Agent': user_agent}

    def reset(self, url):
        self._url = url
        self._driver = None
        self._cookies = {}

    def _dynamic(self):
        # 创建谷歌浏览器驱动参数对象
        chrome_options = webdriver.ChromeOptions()
        # 不加载图片
        # preferences = {"profile.managed_default_content_settings.images": 2}
        # chrome_options.add_experimental_option("prefs", preferences)
        # 使用headless无界面浏览器模式
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # 加载谷歌浏览器驱动
        driver = webdriver.Chrome(options=chrome_options, executable_path="D:\\browserDriver\\chromedriver.exe")
        # 隐式等待
        driver.implicitly_wait(10)
        # 请求地址
        driver.get(self._url)
        return driver

    def login(self, data: dict):
        if self._driver is None:
            self._driver = self._dynamic()
        login_in = self._driver.find_element_by_xpath(data['login_name_xpath'])
        login_in.send_keys(data['name'])
        passwd = self._driver.find_element_by_xpath(data['passwd_xpath'])
        passwd.send_keys(data['passwd'])
        self._driver.find_element_by_xpath(data['submit_xpath']).click()
        time.sleep(15)
        self._driver.refresh()
        cookies_dict = self._driver.get_cookies()
        for cookie in cookies_dict:
            self._cookies[cookie['name']] = cookie['value']
        # print([key + ": " + value for key, value in self.cookies.items()])

    def get_static_raw(self, url, encoding='utf-8'):
        response = requests.get(url, headers=self._headers, cookies=self._cookies)
        response.encoding = encoding
        return response.text

    def get_static(self, url, encoding='utf-8'):
        response = requests.get(url, headers=self._headers, cookies=self._cookies)
        response.encoding = encoding
        return etree.HTML(response.text)

    def get_static_elements(self, url, xpath):
        """获取同一域名下的url 静态的不保存"""
        html = self.get_static(url)
        return html.xpath(xpath)

    def get_dynamic_elements(self, xpath):
        if self._driver is None:
            self._driver = self._dynamic()
        return self._driver.find_elements_by_xpath(xpath)

    def get_dynamic_element(self, xpath):
        if self._driver is None:
            self._driver = self._dynamic()
        return self._driver.find_element_by_xpath(xpath)

    @staticmethod
    def run(func, url_list, ua=ua1):
        """需要一个接受news, url 和 res 列表为参数的func"""
        result = []
        threads = []
        for cur_url in url_list:
            news_parser = NewsParser(cur_url, ua)
            t = Thread(target=func, args=(news_parser, cur_url, result))
            threads.append(t)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return result


if __name__ == '__main__':
    # news_manager = NewsParser("https://weibo.com/", ua1)
    # news_manager.login(
    #     {'name': 18851863569, 'passwd': 'datascience123', 'login_name_xpath': "//input[@id='loginname']",
    #      'passwd_xpath': "//input[@type='password']",
    #      'submit_xpath': "//a[@suda-data='key=tblog_weibologin3&value=click_sign']"})
    print(parse_cookies(
        "SINAGLOBAL=6196500630125.1875.1603275403766; WBPSESS=D9XkFtGB_kQY1AaQKjY4KxF8mH5Qh2OJOM5Z_9fP_ibpoZV60Avg-_Ynp4AjRdhlxZ0tAZlZxuvGr3CH7PLY90SvYLx9NYbowJNwy3SpinBIoQbOMfMilBoozBBk3mDs; SCF=AsQMuAlPE5Vc3YP5BtiLD-n2MKWM-tft5wIzbqI2NM3sU2kiwd6i3c-uInFbnVlB6bamNeHu4r0ftWCAFE0EHbM.; login_sid_t=1a11784b5d2b27dfa353cd776f69babb; cross_origin_proto=SSL; _s_tentry=-; Apache=8077195610521.315.1608106986826; ULV=1608106986830:4:3:2:8077195610521.315.1608106986826:1608099195727; WBtopGlobal_register_version=91c79ed46b5606b9; UOR=,,www.google.com; wb_view_log=1280*8002; WBStorage=8daec78e6a891122|undefined; SUB=_2A25y3iuuDeRhGeFL6FcY9ybJyT-IHXVRqhpmrDV8PUNbmtAKLWimkW9NQjLCa1nMP2-ApBXuu8xF_TDpJybhI8kG; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW2OoyHMADPdokNfi51qOZR5JpX5KzhUgL.FoMfe0-4S0nfeoe2dJLoI0xuMCH8SEHFeb-R1CH81F-R1CHFebH8SCHWSFHWSEH8SE-RBEHWBbH8SE-RBEHWBo5E1Kef; ALF=1639681915; SSOLoginState=1608145916; wvr=6; wb_view_log_7535978523=1280*8002; webim_unReadCount=%7B%22time%22%3A1608146212814%2C%22dm_pub_total%22%3A2%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A2%2C%22msgbox%22%3A0%7D"))
    # with open("./debug.log", 'w') as f:
    #     f.write(str(parse_cookies(
    #         "SINAGLOBAL=6196500630125.1875.1603275403766; WBPSESS=D9XkFtGB_kQY1AaQKjY4KxF8mH5Qh2OJOM5Z_9fP_ibpoZV60Avg-_Ynp4AjRdhlxZ0tAZlZxuvGr3CH7PLY90SvYLx9NYbowJNwy3SpinBIoQbOMfMilBoozBBk3mDs; SCF=AsQMuAlPE5Vc3YP5BtiLD-n2MKWM-tft5wIzbqI2NM3sU2kiwd6i3c-uInFbnVlB6bamNeHu4r0ftWCAFE0EHbM.; login_sid_t=1a11784b5d2b27dfa353cd776f69babb; cross_origin_proto=SSL; _s_tentry=-; Apache=8077195610521.315.1608106986826; ULV=1608106986830:4:3:2:8077195610521.315.1608106986826:1608099195727; WBtopGlobal_register_version=91c79ed46b5606b9; UOR=,,www.google.com; wb_view_log=1280*8002; WBStorage=8daec78e6a891122|undefined; SUB=_2A25y3iuuDeRhGeFL6FcY9ybJyT-IHXVRqhpmrDV8PUNbmtAKLWimkW9NQjLCa1nMP2-ApBXuu8xF_TDpJybhI8kG; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW2OoyHMADPdokNfi51qOZR5JpX5KzhUgL.FoMfe0-4S0nfeoe2dJLoI0xuMCH8SEHFeb-R1CH81F-R1CHFebH8SCHWSFHWSEH8SE-RBEHWBbH8SE-RBEHWBo5E1Kef; ALF=1639681915; SSOLoginState=1608145916; wvr=6; wb_view_log_7535978523=1280*8002; webim_unReadCount=%7B%22time%22%3A1608146212814%2C%22dm_pub_total%22%3A2%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A2%2C%22msgbox%22%3A0%7D")))
