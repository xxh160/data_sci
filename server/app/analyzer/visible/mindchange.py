from matplotlib.font_manager import FontProperties
import  pandas as pd
import matplotlib.pyplot as plt
def paint():
    data=pd.read_csv('/Users/yuanjunping/PycharmProjects/datascience/results/mindchange.csv')
    dic=dict()
    for i in data.values:
        dic[i[0][6:]]=i[1:5]
    lst=[0,0,0,0]
    for i in dic:
        for j in range(0,4):
            lst[j]+=float(dic[i][j])
    print(lst)
    average=sum(lst)/(4 * len(dic))
    lst=[average/(i/len(dic)) for i in lst]
    # for i in dic:
    #     dic[i]=[dic[i][j]*lst[j] for j in range(0,4)]     #加权计算
    x=dic.keys()
    font=FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
    y1=[dic[i][0] for i in x]
    y2=[dic[i][1] for i in x]
    y3=[dic[i][2] for i in x]
    y4=[dic[i][3] for i in x]
    ax=plt.subplot(111)
    plt.title('疫情下的大众心态变化',fontproperties=font)
    plt.xlabel('时间',fontproperties=font)
    plt.ylabel('强度',fontproperties=font)
    ax.plot(x,y1,label='支持 关心 自豪',marker='x')
    ax.plot(x,y2,label='调侃，开心，玩梗',marker='o')
    ax.plot(x,y3,label='对其他地区的不喜欢 对公知的厌恶',marker='*')
    ax.plot(x,y4,label='担心，害怕',marker='.')
    ax.legend(prop=font)
    plt.show()
paint()