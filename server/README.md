# 说明文档

数据科学大作业后端文档

## 总体架构

后端分为三大部分：

- `scraper`即数据获取模块；
- `pretreatment`即数据预处理模块；
- `analysis`即数据分析模块。

数据获取模块异步获取数据，放入其`store`文件夹下。

数据预处理模块异步从数据获取模块获取数据，将数据源从数据获取模块中删除，并把处理过后的数据放入其`store`文件夹下。

数据分析模块异步从数据预处理模块获取数据，将数据源从数据预处理模块中删除，并把处理过后的数据放入其`store`文件夹下。

其中，数据分析模块和前端进行交互，进行数据可视化。

具体描述见各自文档。

## doc

- [`scraper`](doc/scraper.md)
- [`pretreatment`](doc/pretreatement.md)
- [`analysis`](doc/analysis.md)
- [`interface`](doc/interface.md)
