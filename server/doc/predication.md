# predication

预测模块。

通过机器学习模型来对评论进行情感分析。

## 标签分类

- good，普遍乐观情绪的代表
- anger，愤怒，较为激进的消极情绪
- suspicion，怀疑，情感极性中等且较特殊的消极情绪
- worry，担忧，普遍的消极情绪

每一种情绪用大约400条数量的评论进行训练。

## 预测

通过第三方库使用多种分类算法进行分类。

### naive byes

通过`pyhanlp`提供的朴素贝叶斯分类算法实现。

具体位于`predict_naive_byes.py`，接口描述如下。

```python
def predict(text: str) -> str:
    """预测结果以文本形式呈现"""
    res = ""
    return res
```

