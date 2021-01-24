import os
from _datetime import date, timedelta

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame

from app.predicator.pyhanlp_predication.predict import Predict

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# stage分类来自《抗击新冠肺炎疫情的中国行动》白皮书
stages = [{"第一阶段：迅即应对突发疫情": [date(2019, 12, 31), date(2020, 1, 19)]},
          {"第二阶段：初步遏制疫情蔓延势头": [date(2020, 1, 20), date(2020, 2, 20)]},
          {"第三阶段：本土新增病例数逐步下降至个位数": [date(2020, 2, 21), date(2020, 3, 17)]},
          {"第四阶段：取得武汉保卫战、湖北保卫战决定性成果": [date(2020, 3, 18), date(2020, 4, 28)]},
          {"第五阶段：全国疫情防控进入常态化": [date(2020, 4, 29), date(2020, 6, 1)]},
          {"总体走势": [date(2019, 12, 31), date(2020, 6, 1)]}]


def store(x: list, y: list, stage: dict, target: str):
    full_path = os.path.join(".\\store\\" + target, target + "_" + list(stage.items())[0][0] + ".csv")
    data = {"x": x, "y": y}
    df = DataFrame(data)
    df.to_csv(full_path, header=0, index=0)


def paint(x: list, y: list, title: str, label: str, y_label: str, x_label: str, full_name: str):
    plt.plot(x, y, "r*:", label=label, linewidth=2)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.ylim([0, 1])
    plt.legend()
    plt.grid()
    plt.title(title)
    plt.xticks(rotation=-45)
    plt.gcf().set_size_inches(25, 15)
    plt.savefig(full_name, dpi=100)
    plt.show()


def load_from_file(path: str, name: str) -> dict:
    full_path = os.path.join(path, name)
    if not os.path.exists(full_path):
        return {}
    df = pd.read_csv(full_path, names=['x', 'y'])
    x = df['x'].tolist()
    y = df['y'].tolist()
    return {'x': x, 'y': y}


def paint_emotion(cur_stage: dict, src_path: str, target: str, predicator: Predict, re: bool,
                  y_description: str) -> str:
    stage_description = list(cur_stage.items())[0][0]
    file_res = load_from_file(".\\store\\" + target, target + "_" + stage_description + ".csv")
    if not re and file_res != {}:
        paint(file_res['x'], file_res['y'], stage_description + " 情绪分析", stage_description, y_description, "时间",
              os.path.join(".\\store\\" + target + "\\img", target + "_" + list(cur_stage.items())[0][0] + ".png")
              )
        print("From file")
        curve(list(range(len(file_res['x']))), file_res['y'],
              os.path.join(".\\store\\" + target + "\\img", target + "_" + list(cur_stage.items())[0][0] + "_fit.png"))
        return str(np.mean(np.array(file_res['y'])))
    stage_dates = list(cur_stage.items())[0][1]
    begin_date = stage_dates[0]
    end_date = stage_dates[1]
    data = []
    index = np.arange(begin_date, end_date + timedelta(days=1))
    real_index = []
    for cur_index in index:
        cur_date = cur_index.item()
        real_index.append(str(cur_date.month) + "-" + str(cur_date.day))
    del_index = []
    cur_num = 0
    while begin_date <= end_date:
        pos_num = 0
        neg_num = 0
        full_path = os.path.join(src_path, target + "_" + str(begin_date) + ".csv")
        begin_date += timedelta(days=1)
        df = None
        try:
            df = pd.read_csv(full_path, error_bad_lines=False, quotechar=None, quoting=3)
        except FileNotFoundError:
            pass
        if df is None or df.empty:
            del_index.append(index[cur_num])
        else:
            column_name = df.columns.values.tolist()[-1]
            for cur_index, cur_value in df.iterrows():
                res = predicator.predict(str(cur_value[column_name]))
                if res == "pos":
                    pos_num += 1
                else:
                    neg_num += 1
            rate = float(pos_num) / float(pos_num + neg_num)
            data.append(rate)
        cur_num += 1
    for cur_date in del_index:
        cur_date = cur_date.item()
        cur_date = str(cur_date.month) + "-" + str(cur_date.day)
        real_index.remove(cur_date)
    store(real_index, data, cur_stage, target)
    paint(real_index, data, stage_description + " 情绪分析", stage_description, y_description, "时间",
          os.path.join(".\\store\\" + target + "\\img", target + "_" + list(cur_stage.items())[0][0] + ".png"))
    curve(list(range(len(real_index))), data,
          os.path.join(".\\store\\" + target + "\\img", target + "_" + list(cur_stage.items())[0][0] + "_fit.png"))
    return str(np.mean(np.array(data)))


def curve(x: list, y: list, full_path: str):
    f1 = np.polyfit(x, y, 3)
    p1 = np.poly1d(f1)
    print(p1)
    y_val = p1(x)
    # 绘图
    plt.plot(x, y, 's', label='original values')
    plt.plot(x, y_val, 'r', label='fit values')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(loc=4)  # 指定legend的位置右下角
    plt.title('fit')
    plt.savefig(full_path)
    plt.show()


if __name__ == '__main__':
    for i in range(1, 6):
        print(paint_emotion(stages[i], "..\\scraper\\store\\bilibili", "bilibili",
                            Predict("outer", ".\\pyhanlp_predication"), True, "积极评论比例"))
        print(paint_emotion(stages[i], "..\\scraper\\store\\weibo", "weibo",
                            Predict("outer", ".\\pyhanlp_predication"), True, "积极评论比例"))
    # print(os.listdir("/"))
    # load_from_file(".\\store\\weibo", "weibo_第二阶段：初步遏制疫情蔓延势头.csv")
