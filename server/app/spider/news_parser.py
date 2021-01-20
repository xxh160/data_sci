import queue
import threading
import time
from queue import Queue

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


class Task(threading.Thread):
    def __init__(self, q: Queue, func):
        threading.Thread.__init__(self)
        self.q = q
        self.func = func

    def run(self) -> None:
        while True:
            try:
                cur_url = self.q.get(block=True, timeout=1)
            except queue.Empty:
                break
            self.func(url=cur_url)
            self.q.task_done()


class NewsParser:
    def __init__(self, url, user_agent):
        self._url = url
        self._driver = None
        self._cookies = {}
        self._headers = {'User-Agent': user_agent, "Connection": "close"}

    @staticmethod
    def run(func, urls: Queue):
        start = time.time()
        for i in range(4):
            cur_task = Task(urls, func)
            cur_task.start()
        urls.join()
        end = time.time()
        print("time: " + str(end - start))

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

    def close(self):
        self._driver.quit()
        self._driver = None

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

    def get_static_raw(self, url, encoding='utf-8'):
        response = requests.get(url, headers=self._headers, cookies=self._cookies, verify=False)
        response.encoding = encoding
        return response.text

    def get_static(self, url, encoding='utf-8'):
        response = requests.get(url, headers=self._headers, cookies=self._cookies, verify=False)
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
