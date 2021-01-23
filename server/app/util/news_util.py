import queue
import threading
import time
from queue import Queue

import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 ' \
     'Safari/537.36 '


def _parse_cookies(cookie_str):
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
        self.url = url
        self.driver = None
        self.cookies = {}
        self.headers = {'User-Agent': user_agent, "Connection": "close"}

    @staticmethod
    def run(func, urls: Queue):
        start = time.time()
        for i in range(1):
            cur_task = Task(urls, func)
            cur_task.start()
        urls.join()
        end = time.time()
        print("time: " + str(end - start))

    def reset(self, url):
        self.url = url
        cookies_list = self.driver.get_cookies()
        valid_list = []
        for cookie in cookies_list:
            cur = {"name": cookie['name'], "value": cookie['value']}
            valid_list.append(cur)
        for cookie in valid_list:
            self.driver.add_cookie(cookie)
        self.driver.get(url)
        self.driver.implicitly_wait(2)

    def dynamic(self) -> WebDriver:
        # 创建谷歌浏览器驱动参数对象
        chrome_options = webdriver.ChromeOptions()
        # 加载谷歌浏览器驱动
        driver = webdriver.Chrome(options=chrome_options, executable_path="D:\\browserDriver\\chromedriver.exe")
        # 隐式等待
        driver.implicitly_wait(10)
        # 请求地址
        driver.get(self.url)
        return driver

    def fast_dynamic(self, valid_list: list) -> WebDriver:
        # 创建谷歌浏览器驱动参数对象
        chrome_options = webdriver.ChromeOptions()
        prefs = {
            'profile.default_content_setting_values': {
                'images': 2
            }
        }
        chrome_options.add_experimental_option("prefs", prefs)  # 加载无图模式设置
        chrome_options.add_argument("--headless")
        # 加载谷歌浏览器驱动
        driver = webdriver.Chrome(options=chrome_options, executable_path="D:\\browserDriver\\chromedriver.exe")
        # 隐式等待
        cur_url = self.url.split(".com")[0] + ".com"
        driver.get(cur_url)
        driver.implicitly_wait(10)
        for cookie in valid_list:
            driver.add_cookie(cookie)
        return driver

    def close(self):
        self.driver.quit()
        self.driver = None

    def login(self, data: dict):
        if self.driver is None:
            self.driver = self.dynamic()
        login_in = self.driver.find_element_by_xpath(data['login_name_xpath'])
        login_in.send_keys(data['name'])
        passwd = self.driver.find_element_by_xpath(data['passwd_xpath'])
        passwd.send_keys(data['passwd'])
        self.driver.find_element_by_xpath(data['submit_xpath']).click()
        time.sleep(15)
        self.driver.refresh()
        cookies_list = self.driver.get_cookies()
        for cookie in cookies_list:
            self.cookies[cookie['name']] = cookie['value']

        # cookies_list = self.driver.get_cookies()
        # valid_list = []
        # for cookie in cookies_list:
        #     cur = {"name": cookie['name'], "value": cookie['value']}
        #     valid_list.append(cur)
        # self.driver.close()
        # self.driver.quit()
        # self.driver = self.fast_dynamic(valid_list)

    def click(self, xpath: str):
        self.driver.find_element_by_xpath(xpath).click()
        self.driver.implicitly_wait(3)

    def get_static_raw(self, url, encoding='utf-8'):
        response = requests.get(url, headers=self.headers, cookies=self.cookies, verify=False)
        response.encoding = encoding
        return response.text

    def get_static(self, url, encoding='utf-8'):
        response = requests.get(url, headers=self.headers, cookies=self.cookies, verify=False)
        response.encoding = encoding
        return etree.HTML(response.text)

    def get_static_elements(self, url, xpath):
        """获取同一域名下的url 静态的不保存"""
        html = self.get_static(url)
        return html.xpath(xpath)

    def get_dynamic_elements(self, xpath):
        if self.driver is None:
            self.driver = self.dynamic()
        return self.driver.find_elements_by_xpath(xpath)

    def get_dynamic_element(self, xpath):
        if self.driver is None:
            self.driver = self.dynamic()
        return self.driver.find_element_by_xpath(xpath)


if __name__ == '__main__':
    # driver = webdriver.Chrome(executable_path="D:\\browserDriver\\chromedriver.exe")
    # driver.get("https://www.baidu.com")
    # # add_cookie method driver
    # driver.add_cookie({"name": "foo", "value": "bar"})
    #
    # print(driver.get_cookies())
    # c = driver.get_cookies()
    # cookies = []
    # for cookie in c:
    #     cur = {"name": cookie['name'], "value": cookie['value']}
    #     cookies.append(cur)
    #
    # print(driver.current_url)
    # driver.get("https://www.sina.com")
    # for cookie in cookies:
    #     driver.add_cookie(cookie)
    # print(driver.current_url)
    # print(driver.get_cookies())
    pass
