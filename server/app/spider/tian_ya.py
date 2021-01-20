import urllib.request

from bs4 import BeautifulSoup


def tian_ya(url):
    list = []
    page = urllib.request.urlopen(url)
    content = page.read()
    soup = BeautifulSoup(content, "html5lib")
    title = soup.find("h1", class_="atl-title")
    if title is not None:
        list.append(title.get_text().strip())
    info = soup.find("div", class_="atl-info")
    if info is not None:
        for tag in info.find_all("span"):
            if "时间" in tag.get_text():
                list.append(tag.get_text())
        list.append(url)
        list.append([])
        for tag in soup.find_all("div", class_="bbs-content"):
            list[3].append(tag.get_text().strip().replace("\u3000", ""))
    return list


def go(url):
    list = []
    page = urllib.request.urlopen(url)
    content = page.read()
    soup = BeautifulSoup(content, "html5lib")
    tag = soup.find("div", class_="searchListOne")
    if tag is not None:
        for target in tag.find_all("a"):
            if "post" in target.get("href"):
                list.append(tian_ya(target.get("href")))
    return list


def get_all():
    list = []
    url = "https://search.tianya.cn/bbs?q=%E6%96%B0%E5%86%A0%E7%96%AB%E6%83%85&"
    page = urllib.request.urlopen(url + "pn=2&f=3")
    content = page.read()
    soup = BeautifulSoup(content, "html5lib")
    maxNum = "0"
    for i in soup.find_all("a"):
        if i.get_text().isdigit():
            maxNum = i.get_text()
        if "下一页" in i.get_text():
            break
    for i in range(2, 1 + int(maxNum)):
        # for i in range(2,3):
        list += go(url + "pn=" + str(i) + "&f=3")
    return list
