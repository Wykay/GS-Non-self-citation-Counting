# Google Scholar Non-self Citation Counting

This program is designed to count the times that a specific paper on google scholar has been cited by other paper whose author list doesn't contain any author of the counted one (i.e. non-self citation list) . It would produce a txt file result/result.txt, containing the info including name, authors, year, publisher of the non-self citation papers, and print the number of IEEE Fellow in the command line.

This program is based on https://github.com/rpSebastian/gs-cite-fellow. Thanks greatly to this author!
[中文简介](https://github.com/facebookresearch/detectron2/blob/d779ea63faa54fe42b9b4c280365eaafccb280d6/detectron2/evaluation/evaluator.py#L164)
## Some cases that the final result may be inaccurate

* The name of author in the citing article is the same as the counted one's.
* DBLP(https://dblp.org) doesn't include some papers' info, but the author lists of all papers are crawled from it.
* The IEEE Fellow list in fellow is not accurate.
* Google Scholar only show 1000 citing papers, so for those whose citing times is grater than 1000, the result may be inaccurate.

## Installation

```
pip install -r requirements.txt
```

## Configuration

Install Google Chrome driver according to your Chrome version， modify these in config.json.

* ``scholar_id``. The scholar's Google Scholar Id, which can be found in the URL of the scholar's Google Scholar home page.
* ``driver_path``. The address of the Google Chrome driver, which must be the same version as Google Chrome. It can be downloaded from the internet.

## Procedure


Remove data/articles_id_0.json （a file recording the info of citing list）

Specifiy which paper is to be counted at the beginning of 02_ ，04_，05_ 

Run scripts 01_ 02_ 03_ 04_05_06_ in order

Run 08_ and the number of IEEE fellows will be printed.

## Result

* result.txt

![image](https://github.com/EvenYYY/GS-other-citations-Crawling-new/blob/main/figures/result.png)
