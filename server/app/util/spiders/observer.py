import json

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.chrome

originurl = 'https://www.guancha.cn/xinguan/list_1.shtml'
userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
headers = {'User-Agent': userAgent}


def GcZ():  # 观察者网爬取主程序
    k = 1
    ans = []
    for j in range(1, 16):
        url = originurl.replace('1', str(j))
        response = requests.get(url=url, headers=headers)
        response.encoding = response.apparent_encoding  # 避免乱码
        bf = BeautifulSoup(response.text, 'html.parser')
        listItems = bf.find_all('h4', attrs={"class": "module-title"})
        for i in listItems:
            # print(j['href'])
            # 找到子标签a的第一个href
            childrenurl = url + i.find('a', target="_blank")['href'] + '#comment'
            chr = requests.get(url=childrenurl, headers=headers)
            chr.encoding = chr.apparent_encoding
            chbf = BeautifulSoup(chr.text, 'html.parser')
            time = chbf.find('div', attrs={'class': 'time fix'})
            time = time.find('span').text
            comm = chbf.find('div', attrs={
                'class': "gc-comment", 'id': "comments-container"}, recursive=True)
            commid = comm['data-id']
            comments = getcomment(commid)
            title = i.text
            list = [title, time, childrenurl, comments]
            ans.append(list)
            # print('第{}条新闻信息下载完成'.format(k))
            k += 1
        # print(list)
    # print('累计下载{}条新闻信息'.format(k))
    return ans


def getcomment(commid):  # 每个子网站爬取评论的函数
    commenturl = "https://user.guancha.cn/comment/cmt-list.json?codeId=482900&codeType=1&pageNo=1&order=1&ff=www"
    commenturl = commenturl.replace('482900', commid)
    commentpage = requests.get(url=commenturl, headers=headers)
    commentjson = json.loads(commentpage.text)
    coments = []
    for i in commentjson['items']:
        coments.append(i['content'])
    return coments
    # print(commentpage.text)


def get_all():
    return GcZ()
