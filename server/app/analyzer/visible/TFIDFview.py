import  csv

import matplotlib
import  pandas as pd
import  matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
def tfidf():
    font = FontProperties(fname='')
    path='/Users/yuanjunping/PycharmProjects/datascience/results/TFIDF.csv'
    count=0
    d=dict
    c=pd.read_csv(path)
    todel=['就是','我们','自己','前来','就是','人中国','','','']
    count=0
    x=[]
    y=[]
    i=0
    while count<10:
        i += 1
        if(c['词语'][i] in todel):
            continue
        x.append(c['词语'][i])
        y.append(c['tfidf值'][i])
        count+=1
    lst1= ['无衣','英雄','辛苦','祖国','口罩']
    lst2=[0.009413448,0.007637154,0.007325065,0.00727074,0.007005126]
    for i in range(0,5):
        x.append(lst1[i])
        y.append(lst2[i])
    x=[x[i] for i in range(0,15)]
    y=[y[i] for i in range(0,15)]
    plt.barh(list(reversed(x)),list(reversed(y)))  # 横放条形图函数 barh
    plt.title('词频tfidf ranking')
    plt.show()
print(matplotlib.matplotlib_fname())
tfidf()
