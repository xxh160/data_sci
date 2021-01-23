import datetime
import urllib.request

from bs4 import BeautifulSoup


def people(url):
    dict = {}
    page = urllib.request.urlopen(url)
    content = page.read()
    soup = BeautifulSoup(content, "html5lib")
    article = soup.find("div", class_="article")
    title = article.find("h1")
    if title is not None:
        dict["topic"] = title.get_text().strip()
    else:
        dict["topic"] = "NoTitle"
    paragraphs = article.find_all("p")
    if paragraphs is not None:
        dict["content"] = ""
        for tag in paragraphs:
            dict["content"] += tag.get_text().strip()
        dict["url"] = url
    return dict


def go(url, end):
    list = []
    page = urllib.request.urlopen(url + end)
    content = page.read()
    soup = BeautifulSoup(content, "html5lib")
    tag = soup.find("div", class_="news")
    if tag is not None:
        for target in tag.find_all("a"):
            list.append(people(url + "/" + target.get("href")))
    return list


def search(date, keyword):
    # keyword 不用？
    datestr = str(date.year)
    if date.month < 10:
        datestr += ("-0" + str(date.month))
    else:
        datestr += ("-" + str(date.month))
    if date.day < 10:
        datestr += ("/0" + str(date.day))
    else:
        datestr += ("/" + str(date.day))
    list = []
    url = "http://paper.people.com.cn/rmrb/html/"
    end = "/nbs.D110000renmrb_01.htm"
    list += go(url + datestr, end)
    return list


if __name__ == "__main__":
    print(search(datetime.date(2021, 1, 20), None))
