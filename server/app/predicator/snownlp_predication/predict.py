from snownlp import SnowNLP


def predict(text: str) -> int:
    s = SnowNLP(text)
    return s.sentiments


if __name__ == '__main__':
    print(predict("武汉加油！"))
    print(predict("垃圾"))
