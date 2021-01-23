import datetime
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import etree

cookie = "_uuid=CA977C90-B626-1ECF-C821-5EABBE41DB1419875infoc; buvid3=2BF98590-9B03-4B1C-8748-9DD76315A0D6143092infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(J|)RuYmlYm0J'uY||)~~uRl; CURRENT_QUALITY=112; sid=c4nky8dy; bp_video_offset_351632898=482211311356370242; fingerprint3=112f165497aa270f7eba1c34ea8d8fd3; fingerprint_s=2689d6474fc87153e7dc59cd9a2c5f45; buvid_fp=2BF98590-9B03-4B1C-8748-9DD76315A0D6143092infoc; buvid_fp_plain=2BF98590-9B03-4B1C-8748-9DD76315A0D6143092infoc; PVID=5; fingerprint=664a68a4027fb32ab3b04d858af2b453; DedeUserID=478282563; DedeUserID__ckMd5=8322b1667e985120; SESSDATA=3a4e1c18%2C1626709917%2C713a4*11; bili_jct=628f17ef4964ebe5062d1189d26abf96"
useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
headers = {
    "cookie": cookie,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66 "}
baseurl = "https://search.bilibili.com/all?keyword=%E7%96%AB%E6%83%85&order=totalrank&duration=0&tids_1=202&page="


class BarrageSpider:
    def __init__(self, bv):
        # 需要一个bv号，在接下来的代码中进行替换操作
        self.bv = bv
        self.video_name = None
        # 不需要登录的弹幕接口地址 只能爬取部分弹幕
        self.barrage_url = 'https://comment.bilibili.com/{}.xml'
        # 需要登陆的弹幕接口地址 根据日期进行分类 需要循环爬取 最后归总数据
        self.date_url = 'https://api.bilibili.com/x/v2/dm/history?type=1&oid={}&date={}'  # 2021-01-01
        # 点击按钮弹出日历的数据接口，这里我们用来作索引
        self.index_url = 'https://api.bilibili.com/x/v2/dm/history/index?type=1&oid={}&month={}'  # 2021-01
        # 在抓包工具中找的一个简洁的请求，里面有我们需要的oid或者是cid
        self.bv_url = 'https://api.bilibili.com/x/player/pagelist?bvid=' + bv + '&jsonp=jsonp'
        # 视频时间获取
        self.video_url = 'https://www.bilibili.com/video/{}'.format(bv)
        # 不需要登录接口的伪装头
        self.comment = {
            'referer': 'https://www.bilibili.com/',
            'user-agent': useragent
        }
        # 需要登录的伪装头 因为需要登录 ip代理已经没有意义了 这里就不再使用IP代理
        self.date_headers = {
            "referer": "https://www.bilibili.com/",
            "origin": "https://www.bilibili.com",
            "cookie": cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66 "
        }

    # 从接口返回的json中获取到我们的cid 注： cid = oid
    def get_cid(self):
        # 定位到数据data中下面的cid
        return requests.get(url=self.bv_url, headers=self.comment).json()['data'][0]['cid']

    def get_video_time(self):
        time_data = requests.get(url=self.video_url, headers=self.comment).text
        video_page = etree.HTML(time_data)
        v_time = video_page.xpath('//div[@class="video-data"]/span[3]/text()')[0].split(' ')[0]
        self.video_name = video_page.xpath('//h1[@class="video-title"]/span/text()')[0]
        return v_time

    # 解析不需要登录的接口 返回类型是xml文件
    def parse_url(self):
        # 获取指定视频的cid/oid
        cid = self.get_cid()
        # 对页面进行伪装请求，这里注意不要转换成text，使用二进制
        response = requests.get(url=self.barrage_url.format(cid), headers=self.comment).content
        # etree解析
        data = etree.HTML(response)
        # 定位到所有的d元素
        barrage_list = data.xpath('//d')
        for barrage in barrage_list:
            # 获取d元素的p属性值
            info = barrage.xpath('./@p')[0].split(',')
            # 获取弹幕内容
            content = barrage.xpath('./text()')[0]
            item = {'出现时间': info[0], '弹幕模式': info[1], '字体大小': info[2], '颜色': info[3], '发送时间': info[4], '弹幕池': info[5],
                    '用户ID': info[6], 'rowID': info[7], '内容': content}
            # 因为这只是一部分弹幕 所以就没有进行持久化存储 没有必要
            print(item)

    # 循环爬取所有弹幕 需要传入month的数据 根据视频发布的日期到现在的所有月份
    def parse_date_url(self, month):
        print('正在爬取{}的数据'.format(self.video_name + month + "月"))
        # 存放爬到的数据
        result = []
        # 获取视频的oid
        oid = self.get_cid()
        # 获取日期索引
        cururl = self.index_url.format(oid, month)
        cururl = requests.get(url=cururl, headers=self.date_headers)
        date_by_month = cururl.json().get('data')
        # 根据日期索引循环请求
        if date_by_month:
            for day in date_by_month:
                # print('{}月份数据下的{}'.format(month, day))
                # 注意还是二进制文件
                r = requests.get(url=self.date_url.format(oid, day), headers=self.date_headers)
                date_page = r.content
                date_data = etree.HTML(date_page)
                # 解析到到所有的d元素
                barrage_list = date_data.xpath('//d')
                # 循环解析数据

                for barrage in barrage_list:
                    # 获取d元素的p属性值
                    # things= barrage.xpath('./@p')[0].split(',')
                    # 获取弹幕内容 并去掉所有空格
                    content = barrage.xpath('./text()')[0].replace(" ", "")
                    item = {'日期': day, '内容': content}
                    # item.get(day).append(content)
                    result.append(item)
        # 返回封装好的数据
        return result

    # 根据现在的时间遍历所有的月份信息
    def parse_month(self):
        start_day = datetime.datetime.strptime(self.get_video_time(), '%Y-%m-%d')
        # end_day=start_day+relativedelta(months=+1)
        end_day = datetime.date.today()
        months = (end_day.year - start_day.year) * 12 + end_day.month - start_day.month
        m_list = []
        for mon in range(start_day.month - 1, start_day.month + months):
            if (mon % 12 + 1) < 10:
                m_list.append('{}-0{}'.format(start_day.year + mon // 12, mon % 12 + 1))
            else:
                m_list.append('{}-{}'.format(start_day.year + mon // 12, mon % 12 + 1))
        return m_list

    # 舍友指导下的一行代码生成词云 编译器自动格式化了 本质还是一行代码
    # def wordCloud(self):
    #     WordCloud(font_path="C:/Windows/Fonts/simfang.ttf", background_color='white', scale=16).generate(" ".join(
    #         [c for c in jieba.cut("".join(str((pd.read_csv('{}弹幕池数据集.csv'.format(self.video_name))['内容']).tolist()))) if
    #          len(c) > 1])).to_file(
    #         "{}词云.png".format(self.video_name))


def bilibili():
    bvs = []
    for i in range(1, 51):
        url = baseurl + str(i)
        response = requests.get(url=url, headers=headers)
        response.encoding = response.apparent_encoding  # 避免乱码
        bf = BeautifulSoup(response.text, 'html.parser')
        divs = bf.find_all('div', attrs={"class": "headline clearfix"})
        for div in divs:
            bv = str(div.find('a')['href'])
            bvs.append(bv[bv.index('B'):bv.index('?')])
    # 输入指定的视频bv号
    datas = []
    count = 0
    for i in range(20, len(bvs)):
        bv_id = bvs[i]
        spider = BarrageSpider(bv_id)
        spider.parse_month()
        word_data = []
        months = spider.parse_month()
        # 循环遍历爬取
        for month in months:
            word = spider.parse_date_url(month)
            word_data.extend(word)
        # if(len(wo/rd_data)==0):
        # continue
        datas.append(word_data)
        # 数据格式化处理 并输出csv格式文件
        data = pd.DataFrame(word_data)
        # data.drop_duplicates(subset=['rowID'], keep='first')
        # 字符集编码需要为utf-8-sig 不然会乱码
        print('正在爬取第{}个视频{}'.format(i + 1, spider.video_name))
        time.sleep(2)
        data.to_csv('./raw/raw' + '{}.csv'.format(spider.video_name), index=False, encoding='utf-8-sig')
    # # 生成词云
    return datas
