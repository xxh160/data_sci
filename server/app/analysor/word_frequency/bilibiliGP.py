import csv
import time
from collections import Counter

import  jieba
import  os
import  json
import  pandas as pd

#统计b站高频词

def gettext():
    data=''
    basepath='/Users/yuanjunping/PycharmProjects/datascience/bilibilidate'
    for i in os.listdir(basepath):
        if i=='.DS_Store':
            continue
        f=open(basepath+'/'+i)
        for i in f.readlines():
            data+=i+'\n'
    f=open('/results/bilibiliAll.txt', 'w')
    f.write(data)
gettext()
cut_words = ""
all_words = ""
data=open('/results/bilibiliAll.txt').read()
newdata=""
for line in data.split('\n'):
    #line.strip('\n')
    seg_list = jieba.cut(line,cut_all=False)
    # print(" ".join(seg_list))
    cut_words = (" ".join(seg_list))
    newdata+=cut_words+'\n'
    all_words += cut_words


# 输出结果
all_words = all_words.split()
print(all_words)

# 词频统计
c = Counter()
for x in all_words:
    if len(x)>1 and x != '\r\n':
        c[x] += 1

# 输出词频最高的前50个词
print('\n词频统计结果：')
for (k,v) in c.most_common(50):
    print("%s:%d"%(k,v))

# 存储数据
name = "/Users/yuanjunping/PycharmProjects/datascience/bilibili词频.csv"
cv = open(name, 'w', encoding='utf-8')
w=csv.writer(cv)
w.writerow(["词语","频率"])
i=0
for (k,v) in c.most_common(len(c)):
    w.writerow([str(k),str(v)])
    i+=1
    if i >10000:
        break
cv.close()