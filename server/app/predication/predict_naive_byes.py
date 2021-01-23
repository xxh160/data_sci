from pyhanlp import *


class Predict:
    IClassifier = JClass('com.hankcs.hanlp.classification.classifiers.IClassifier')
    NaiveBayesClassifier = JClass('com.hankcs.hanlp.classification.classifiers.NaiveBayesClassifier')

    def __init__(self, path):
        self.i_classifier1 = Predict.NaiveBayesClassifier()
        self.i_classifier1.train(path)

    def predict(self, text):
        res = self.i_classifier1.classify(text)
        # print("\'{}\' 的情感是 {}".format(text, res))
        return res


if __name__ == '__main__':
    test = Predict(".\\lan_lib")
    a = test.predict("请通报湖北省其他地级市把！！！ 只要湖北省离武汉近的地方跟武汉的人员有一大半都是互通的！我家这边一半的车都是鄂A"
                     "的车牌号！！！这些城市到现在还不公布死亡人数感染人数！只字不提！湖北省不是只有一个城市武汉好吗！口罩完全买不到！检测试纸现在还没有也没人管！湖北省正式更名武汉省了吗？")
    b = test.predict("为啥子就喜欢乱跑这些人，不把所有人害死不罢休吗")
    c = test.predict("可利用文本分类实现情感分析，效果行")
    d = test.predict("我好害怕")
    e = test.predict("怎么会这样")
    f = test.predict("造谣的人，用心险恶")
    g = test.predict("这他妈都是些什么嘴！先是你🐴 乱吃的，现在是你🐴 乱说的！")
    h = test.predict("钟南山")
    print(a, b, c, d, e, f, g, h)
