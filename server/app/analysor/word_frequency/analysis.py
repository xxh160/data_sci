import csv
import functools
from collections import Counter
import  datetime
import jieba
import  os
import  pandas as pd
from matplotlib.font_manager import FontProperties
from matplotlib import rcParams
import matplotlib as plt


from 数据分析.Mindset import mset
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置

rcParams['font.family'] = 'sans-serif '
rcParams['font.sans-serif'] = ['Tahoma']
path='/Users/yuanjunping/PycharmProjects/datascience/bilibilidate'
targetpath='/Users/yuanjunping/PycharmProjects/datascience/bilibilidateCP'
def dateCP(): #将bilibilidate下的文件分词并统计各种词语的词频 方便计算每天的心态 （按时间分类）
    for i in os.listdir(path):
        cut_words = ""
        all_words = ""
        datapath=path+'/'+str(i)
        data = open(datapath).read()
        newdata = ""
        for line in data.split('\n'):
            # line.strip('\n')
            seg_list = jieba.cut(line, cut_all=False)
            # print(" ".join(seg_list))
            cut_words = (" ".join(seg_list))
            newdata += cut_words + '\n'
            all_words += cut_words
        # 输出结果
        all_words = all_words.split()
        # 词频统计
        c = Counter()
        for x in all_words:
            if len(x) > 1 and x != '\r\n':
                c[x] += 1
        # 存储数据
        name = targetpath+'/'+str()
        cv = open(name, 'w', encoding='utf-8')
        w = csv.writer(cv)
        w.writerow(["词语", "频率"])
        j = 0
        for (k, v) in c.most_common(len(c)):
            w.writerow([str(k), str(v)])
            j+= 1
            if j > 10000: #只统计出现频率前1000的词
                break
        cv.close()
def analys():
    m=mset()
    d=dict() # 映射关系为日期-》[各种情绪值]
    count=0
    p=os.listdir(targetpath)
    prei=''
    wordnum=0
    p=sorted(p,key=functools.cmp_to_key(cmp2))
    for i in p:
        name=targetpath+'/'+str(i)
        c=pd.read_csv(name)
        if(count==0):
            d[i[0:10]]=[0,0,0,0]
            prei=i
        for pair in c.values:
            wordnum+=int(pair[1])
            for j in range(0,4): #每个情绪词典
                for word in mset.getmset(self=mset)[j] :  #情绪词典里面的每个词
                    word=str(word)
                    mindword=str(pair[0])
                    if(mindword==word or mindword.__contains__(word) or word.__contains__(mindword)):
                       d[prei[0:10]][j]+=pair[1]
                       continue
        count+=1
        if(count==14 or i=='2020-06-29.csv'):     #七天周期结束
            d[prei[0:10]]=[int(x)/wordnum for x in d[prei[0:10]]]
            wordnum=0
            count=0
    f = open('/results/mindchange.csv', 'w')
    c = csv.writer(f)
    c.writerow(["日期", "对国家的关心 支持 自豪 以及希望 祝愿", "调侃 开心 玩梗", "对大陆以外地区的嘲讽，不喜欢，对国内一些人的厌恶", "对疫情的担心 忧虑，恐惧"])
    for i in d:
        l = d[i]
        c.writerow([i[0:10], l[0], l[1], l[2], l[3]])
def cmp2(a,b):
    a=str(a).split('.')[0]
    b=str(b).split('.')[0]
    a = [int(i) for i in str(a).split('-')]
    b = [int(i) for i in str(b).split('-')]
    timea = datetime.date(a[0], a[1], a[2])
    timeb = datetime.date(b[0], b[1], b[2])
    if (timea.__ge__(timeb)):
        return 1
    return -1
# def cmp(a,b):
#     a=a[0]
#     b=b[0]
#     a=[int(i) for i in str(a).split('-')]
#     b=[int(i) for i in str(b).split('-')]
#     timea=datetime.date(a[0],a[1],a[2])
#     timeb=datetime.date(b[0],b[1],b[2])
#     if(timea.__ge__(timeb)):
#         return 1
#     return  -1
