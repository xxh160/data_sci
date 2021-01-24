# encoding: utf-8
import json

import  wordcloud
import  numpy as np
import PIL.Image as image
import  os


def MonthciCloud():  #根据月份生成词云b站 每两个月为一组
    path= '/bilibilidate'
    dir=os.listdir(path)
    dic=dict()
    for i in range(1,4):
        dic[i]=''
    for file in dir:
        j=file[6]
        dic[int((int(j)+1)/2)]+=open(path+'/'+file).read()
    color=['black','black','blue']
    for i in range(1,4):
        mask=np.array(image.open('/mask.jpg'))
        w = wordcloud.WordCloud(font_path='/System/Library/Fonts/PingFang.ttc' ,
                                background_color='white',
          max_font_size=35
)
        d=dic[i].decode('utf-8')
        w.generate(d)
        w.to_file("{}阶段".format(i)+"ciCloud"+".png")
#输入文件夹的绝对路径
#ciCloud('/Users/yuanjunping/PycharmProjects/datascience/bilibilidate')
# bilibilidate='lalala asasa 我不要 我要砍人了'
def bilibiliall():
    bilibiliallpath='/Users/yuanjunping/PycharmProjects/datascience/results/txt'
    mask=np.array(image.open('/mask.jpg'))
    w=wordcloud.WordCloud(font_path='/System/Library/Fonts/PingFang.ttc',mask=mask,max_font_size=50)
    s=open(bilibiliallpath).read()
    d=dict()
    for line in s.split('\n'):
        a=line.split(' ')[0]
        b=line.split(' ')[1]
        d[a]=b
    d=json.dumps(d,ensure_ascii=False)
    d=json.loads(d)
    w.generate_from_frequencies(d)
    w.to_file("b站词云.png")

MonthciCloud()