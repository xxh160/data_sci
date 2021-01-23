import datetime
import time
import urllib.request

from bs4 import BeautifulSoup
from selenium import webdriver


def nanfang(url):
    dict = {}
    page = urllib.request.urlopen(url)
    content = page.read()
    soup = BeautifulSoup(content, "html5lib")
    title = soup.find("h2", id="article_title")
    if (title != None):
        dict["topic"] = (title.get_text().strip())
    else:
        dict["topic"] = ("NoTitle")
    cont = soup.find("div", class_="content")
    if (cont != None):
        texts = cont.find_all("p")
        dict["content"] = ""
        if (texts != None):
            for text in texts:
                dict["content"] += "\n" + text.get_text()
        dict["url"] = url
    return dict


def go(url):
    browser = webdriver.Chrome(executable_path="D:\\browserDriver\\chromedriver.exe")
    browser.get(url)
    time.sleep(2)
    list = []
    soup = BeautifulSoup(browser.page_source, "html5lib")
    tag = soup.find("div", class_="result-box")
    if (tag != None):
        for target in tag.find_all("a"):
            list.append(nanfang(target.get("href")))
    else:
        print("None")
    browser.close()
    return list


def search(date, keyword):
    keyword = urllib.parse.quote(keyword)
    datestr = str(date.year)
    if (date.month < 10):
        datestr += ("-0" + str(date.month))
    else:
        datestr += ("-" + str(date.month))
    if (date.day < 10):
        datestr += ("-0" + str(date.day))
    else:
        datestr += ("-" + str(date.day))
    list = []
    page = "1"
    url = "http://www.southcn.com/search/pc/advresult.html?keyword=" + \
          keyword + "&size=10&from=" + datestr + "&to=" + datestr + "&o=desc&page="
    end = "&category=%E5%8D%97%E6%96%B9%E7%BD%91pc%E7%AB%AF"
    browser = webdriver.Chrome(executable_path="D:\\browserDriver\\chromedriver.exe")
    browser.get(url + page + end)
    time.sleep(3)
    soup = BeautifulSoup(browser.page_source, "html5lib")
    maxNum = "0"
    for i in soup.find_all("a"):
        if (i.get_text().isdigit()):
            maxNum = i.get_text()
        if ("末页" in i.get_text()):
            maxNum = i.get("data-page")
            break
    browser.close()
    for i in range(1, 1 + int(maxNum)):
        # for i in range(1, 2):
        list += go(url + str(i) + end)
    return list


if __name__ == "__main__":
    print(search(datetime.date(2021, 1, 1), "疫情"))
