from pyhanlp import *


class Predict:
    """朴素贝叶斯模型"""
    NaiveBayesClassifier = SafeJClass('com.hankcs.hanlp.classification.classifiers.NaiveBayesClassifier')
    IOUtil = SafeJClass('com.hankcs.hanlp.corpus.io.IOUtil')

    def __init__(self, lan_path):
        self.i_classifier1 = self.train_or_load_classifier(lan_path, "model.ser", ".")

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


if __name__ == '__main__':
    test = Predict("../lan_lib")
    test.retrain("../lan_lib")
    print(test.predict("哈哈哈哈哈哈"))
