import pandas as pd
from pyhanlp import *


class Predict:
    """朴素贝叶斯模型"""
    NaiveBayesClassifier = SafeJClass('com.hankcs.hanlp.classification.classifiers.NaiveBayesClassifier')
    IOUtil = SafeJClass('com.hankcs.hanlp.corpus.io.IOUtil')

    def __init__(self, lan_path, model_path):
        self.i_classifier1 = self.train_or_load_classifier(lan_path, "model.ser", model_path)

    @staticmethod
    def train_or_load_classifier(lan_path: str, model_name: str, model_path: str):
        model_name = os.path.join(model_path, model_name)
        if os.path.isfile(model_name):
            return Predict.NaiveBayesClassifier(IOUtil.readObjectFrom(model_name))
        classifier = Predict.NaiveBayesClassifier()
        classifier.train(lan_path)
        model = classifier.getModel()
        IOUtil.saveObjectTo(model, model_name)
        return Predict.NaiveBayesClassifier(model)

    def retrain(self, lan_path: str):
        model_name = "model.ser"
        model_path = "."
        model_name = os.path.join(model_path, model_name)
        classifier = Predict.NaiveBayesClassifier()
        classifier.train(lan_path)
        model = classifier.getModel()
        IOUtil.saveObjectTo(model, model_name)
        self.i_classifier1 = Predict.NaiveBayesClassifier(model)

    def predict(self, text):
        res = self.i_classifier1.classify(text)
        return res

    def predict_file(self, path: str, name: str):
        full_path = os.path.join(path, name)
        df = None
        try:
            df = pd.read_csv(full_path, error_bad_lines=False, quotechar=None, quoting=3)
        except FileNotFoundError:
            pass
        if df is None or df.empty:
            pass
        else:
            column_name = df.columns.values.tolist()[-1]
            for cur_index, cur_value in df.iterrows():
                res = self.i_classifier1.classify(str(cur_value[column_name]))
                print(str(cur_value[column_name]), res)


if __name__ == '__main__':
    test = Predict("../outer", ".")
    test.retrain("../lan_lib")
    print(test.predict("垃圾"))
    # test.predict_file("..\\..\\pretreater\\store\\bilibili", "bilibili_2020-01-26.csv")
