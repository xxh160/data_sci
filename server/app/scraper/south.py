import requests
import urllib.request
import re
import datetime
import time
from pandas import DataFrame
from bs4 import BeautifulSoup
from distutils.filelist import findall
from selenium import webdriver
from _datetime import timedelta


def nanfang(url):
    dict = {}
    dict["content"] = ""
    dict["url"] = url
    dict["topic"] = "NoTitle"
    try:
        page = urllib.request.urlopen(url)
        content = page.read()
        soup = BeautifulSoup(content, "html5lib")
        title = soup.find("h2", id="article_title")
        if(title != None):
            dict["topic"] = (title.get_text().strip())
        cont = soup.find("div", class_="content")
        if(cont != None):
            texts = cont.find_all("p")
            if(texts != None):
                for text in texts:
                    dict["content"] += "\n"+text.get_text()
    except:
        pass
    return dict


def go(url):
    browser = webdriver.Firefox()
    browser.get(url)
    time.sleep(2)
    list = []
    soup = BeautifulSoup(browser.page_source, "html5lib")
    tag = soup.find("div", class_="result-box")
    if(tag != None):
        for target in tag.find_all("a"):
            list.append(nanfang(target.get("href")))
    else:
        print("None")
    browser.close()
    return list


def search(date, keyword):
    keyword = urllib.parse.quote(keyword)
    datestr = str(date.year)
    if(date.month < 10):
        datestr += ("-0"+str(date.month))
    else:
        datestr += ("-"+str(date.month))
    if(date.day < 10):
        datestr += ("-0"+str(date.day))
    else:
        datestr += ("-"+str(date.day))
    list = []
    page = "1"
    url = "http://www.southcn.com/search/pc/advresult.html?keyword=" + \
        keyword+"&size=10&from="+datestr+"&to="+datestr+"&o=desc&page="
    end = "&category=%E5%8D%97%E6%96%B9%E7%BD%91pc%E7%AB%AF"
    browser = webdriver.Firefox()
    browser.get(url+page+end)
    time.sleep(3)
    soup = BeautifulSoup(browser.page_source, "html5lib")
    maxNum = "0"
    for i in soup.find_all("a"):
        if(i.get_text().isdigit()):
            maxNum = i.get_text()
        if("末页" in i.get_text()):
            maxNum = i.get("data-page")
            break
    browser.close()
    for i in range(1, 1+int(maxNum)):
        # for i in range(1, 2):
        list += go(url+str(i)+end)
    dic = {"topic": [], "content": [], "url": []}
    for i in range(1, len(list)):
        dic["topic"].append(list[i]["topic"])
        dic["content"].append(list[i]["content"])
        dic["url"].append(list[i]["url"])
    return dic


def run(begin_time, end_time, keywords):
    while begin_time <= end_time:
        print(begin_time)
        cur_res = search(begin_time, keywords)
        df = DataFrame(cur_res)
        df.to_csv("./store/south/" + "south_" + str(begin_time) + ".csv")
        begin_time += timedelta(days=1)


if(__name__ == "__main__"):
    run(datetime.date(2020, 6, 3), datetime.date(2020, 6, 15), "疫情")
    # print(search(datetime.date(2021,1,1),"疫情"))
