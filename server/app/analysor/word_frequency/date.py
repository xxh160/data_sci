import  datetime
import  csv
import  os
import  pandas as pd
import  re
#将弹幕按照时间分类
r='20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
startday=datetime.date(2019,12,8)
endday=datetime.date(2020,6,30)
dic=dict()
basepath = '/Users/yuanjunping/PycharmProjects/datascience/bilibilidate'
for i in os.listdir(basepath):
    if i == '.DS_Store':
        continue
    csvpath = basepath + '/' + i
    print(csvpath)
    datas = pd.read_csv(csvpath)
    for j in datas.values:
        if(re.match(r,j[0])==False):
            continue
        d=[int(i) for i in str(j[0]).split('-')]
        CommentDate=datetime.date(d[0],d[1],d[2])
        if(CommentDate.__le__(startday) or CommentDate.__ge__(endday)):
            continue
        if(dic.keys().__contains__(j[0])==False):
            dic[j[0]] = []
        k=dic[j[0]]
        dic[j[0]].append(j[1])
targetpath='/Users/yuanjunping/PycharmProjects/datascience/bilibilidate'
for i in dic:
        f=open(targetpath+'/'+str(i),'w')
        for j in dic[i]:
            f.write(str(j)+'\n')
        f.close()

