# coding=utf-8
import os
from collections import Counter
import  csv
from math import log
import jieba.analyse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.font_manager import FontProperties
#对b站数据进行tfidf分析 先生成每个视频的词语到频率的映射 然后计算
def GetCP(path,count):  #path csv path
    if(count==10):
        count=10
    cut_words = ""
    all_words = ""
    c=pd.read_csv(path)
    data=''
    for i in c['内容']:
        data+=str(i)+'\n'
    newdata = ""
    for line in data.split('\n'):
        # line.strip('\n')
        seg_list = jieba.cut(line, cut_all=False)
        # print(" ".join(seg_list))
        cut_words = (" ".join(seg_list))
        newdata += cut_words + '\n'
        all_words += cut_words

    all_words = all_words.split()
    # 词频统计
    c = Counter()
    for x in all_words:
        if len(x) > 1 and x != '\r\n':
            c[x] += 1
    # 输出词频最高的前50个词
    # 存储数据
    name = "/Users/yuanjunping/PycharmProjects/datascience/videoCP"+'/'+str(count)
    cv = open(name, 'w', encoding='utf-8')
    w = csv.writer(cv)
    w.writerow(["词语", "频率"])
    i = 0
    for (k, v) in c.most_common(len(c)):
        w.writerow([str(k), str(v)])
        i += 1
        if i > 100:
            break
    cv.close()

def TFIDF(path):  #path为存放文件的目录 csv文件
    filenum=0
    for i in os.listdir(path) :
        if(i=='.DS_Store'):
            continue
        csvpath=path+'/'+i
        GetCP(csvpath,filenum)
        filenum+=1   #每个文章的词频 方便计算tf-idf 跑一次后就可以注释掉了
    videopath='/Users/yuanjunping/PycharmProjects/datascience/videoCP'
    d=dict()  #字典内为 词语->【出现的次数，出现的文章数】
    filenum=0
    wordnum=0
    for i in os.listdir(videopath):
        filenum+=1
        csvpath=videopath+'/'+i
        c=pd.read_csv(csvpath)
        for j in c.values:
            wordnum+=j[1]
            if(d.keys().__contains__(j[0])==False):
                d[j[0]]=[j[1],1]
            else :
                d[j[0]][0]+=j[1] #词频数加
                d[j[0]][1]+=1 #文章数加一
    todel=[]
    for word in d:
        cp=d[word][0]
        filep=d[word][1]
        if(cp<30):
            todel.append(word)
        tfidf=(cp/wordnum)*log((filenum/filep+1))
        d[word]=tfidf
    for word in todel:
        del d[word]
    d= sorted(d.items(), key = lambda x:x[1],reverse=True) #排序
    tfidfpath='/Users/yuanjunping/PycharmProjects/datascience/results/TFIDF.csv'
    c=open(tfidfpath,'w')
    w=csv.writer(c)
    w.writerow(['词语','tfidf值'])
    f=open("/Users/yuanjunping/PycharmProjects/datascience/百度停词表.txt")
    f=f.readlines()
    for word in d:
        if word in f:
            continue  #去除停用词
        w.writerow([word[0],word[1]])
    print(d)
TFIDF('/Users/yuanjunping/PycharmProjects/datascience/bilibili')




