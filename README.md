# Google Scholar 文章他引数量

本程序用于对Google Scholar 上指定的一篇文章统计其引用里的他引文章数量，并输出这些他引文章的名称、作者列表、年份、发表位置至 result/result.txt 里，并在命令行输出所以他引文章中有多少个IEEE Fellow

本程序基于https://github.com/rpSebastian/gs-cite-fellow 完成，十分感谢这位作者的工作！

## 会出错的一些情况

* 引用文章的作者名字和爬取文章的作者名字相同
* DBLP 网站没有收录到一些文章的信息，无法查询其作者，进而无法做他引判断
* Fellow 名单不全
* Google Scholar 只显示引用列表里的1000个结果，对于引用数超过1000的文章统计会出错

## 安装

```
pip install -r requirements.txt
```

## 配置

安装与chrome版本匹配的Google Chrome driver， 将以下信息添加到 config.json ``.

* ``scholar_id``. The scholar's Google Scholar Id, which can be found in the URL of the scholar's Google Scholar home page.
* ``driver_path``. The address of the Google Chrome driver, which must be the same version as Google Chrome. It can be downloaded from the internet.

## 执行过程

#流程：  先按github指示配置config.json里面的scholar_id和 chromedriver.exe在系统的路径

删除data文件夹下的 articles_id_0.json 文件

再依次执行01_ 02_ 03_ 04_05_06_的 py 文件，其中02_ ，04_，05_开头需要指定哪篇论文

最后执行08_ 会在命令行输出 fellow 数量，08_程序可能需要稍微修改，因为之前做的仓促，代码可能有点乱，有一点BUG要调整一下，还请大家见谅！！！

## 结果

* result.txt

![](https://github.com/EvenYYY/GS-other-citations-Crawling-new/blob/main/figures/result.png)

