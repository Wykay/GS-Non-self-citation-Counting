# Google Scholar Non-self Citation Counting

This program is designed to count the times that a specific paper on google scholar has been cited by other paper whose author list doesn't contain any author of the counted one (i.e. non-self citation list) . It would produce a txt file result/result.txt, containing the info including name, authors, year, publisher of the non-self citation papers, and print the number of IEEE Fellow in the command line.

This program is based on https://github.com/rpSebastian/gs-cite-fellow . Thanks greatly to this author !

## Some cases that the final result may be inaccurate

* The name of author in the citing article is the same as the counted one's.
* DBLP(https://dblp.org) doesn't include some papers' info, but the author lists of all papers are crawled from it.
* The IEEE Fellow list in fellow is not accurate.
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

删除data文件夹下的 articles_id_0.json 文件（在每次执行02后产生，记录的为爬取文章的作者的所有论文信息）

再依次执行01_ 02_ 03_ 04_05_06_的 py 文件，其中02_ ，04_，05_开头需要指定哪篇论文

最后执行08_ 会在命令行输出 fellow 数量

## 结果

* result.txt

![image](https://github.com/EvenYYY/GS-other-citations-Crawling-new/blob/main/figures/result.png)
