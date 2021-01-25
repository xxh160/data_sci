from snownlp import SnowNLP


def predict(text: str) -> int:
    s = SnowNLP(text)
    return s.sentiments


def extract_keywords(text: str):
    s = SnowNLP(text)
    return s.keywords(3)


def extract_file_keywords(path: str, name: str):
    pass


if __name__ == '__main__':
    print(predict("武汉加油！"))
    print(predict("垃圾"))
    print(extract_keywords("你他妈的说什么鬼东西呢你个没娘养的东西"))
