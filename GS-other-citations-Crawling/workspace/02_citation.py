#对作者的每篇文章：爬取引用该文章的所有文章的标题，保存在articles.json里面

#**********指定参数：
target_id = 50    #要爬取google scholar 主页上的第几篇(从0开始）


import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By        #按照各种元素如ID NAME CSS_SELECTOR定位元素
from bs4 import BeautifulSoup         #爬取数据的库
import time
import json
import sys
from utils import load_json, save_json


def main():

    d = open_browser()                            #打开浏览器，爬取
    articles = load_json("data/articles.json")
    new_articles = articles.copy()                     #对作者所有文章复制一份
    for article_id, info in enumerate(articles):       #对作者的每篇文章



#-----------------只爬取第17篇论文-----------------------------
        if  article_id != target_id :                         #只爬取第target_id+1篇的引用
            continue
 # -----------------只爬取第17篇论文-----------------------------

        base_url = info["cite_url"]                    # ”引用“ 界面
        name = info["name"]                            #  该文章名字
        get_all_cite_name_list(d, base_url, name, article_id, new_articles)
        print('爬取完成')

#get_all_cite_name_list只爬取名字
def get_all_cite_name_list(d, base_url, name, article_id, new_articles):
    all_cite_name_list = []    #每篇文章的被引用列表
    for start in range(0, 100000, 10):
        print("Page {}".format(start // 10))
        url = get_specify_url(base_url, start)    #每一页引用文章列表的网址，数字按10递增，因为每页显示10篇引用文章
        enter_url(d, url)                         #打开该页                           *******引用文章列表界面
        cite_name_list = get_cite_name_list(d)    #获取该页的引用文章列表
        if len(cite_name_list) == 0:
            break
        all_cite_name_list.extend(cite_name_list)  #把该页引用文章插入总引用列表

        new_articles[article_id]["cite_list"] = []                #创建该篇paper的引用列表
        for cite_name in all_cite_name_list:
            new_articles[article_id]["cite_list"].append({"title": cite_name})
            print(cite_name)
        save_json(new_articles, "data/articles.json")     #保存了每篇文章的引用列表（名字）


def open_browser():         #打开浏览器
    print("start openning browser")
    config = load_json("config.json")
    d = webdriver.Chrome(executable_path=config["driver_path"])
    d.set_window_size(1400, 800)
    print("finish openning browser")
    return d


def get_specify_url(base_url, start):           #获取每一页引用list的网址
    url = base_url.replace("oi=bibs", "start={}".format(start))    #用整数10 20 30等替换 字符串 oi=bibs，形成每页网址
    return url



def enter_url(d, url):
    print("start getting url", url)
    d.get(url)
    time.sleep(1)
    print("finish getting url", url)
    check_verification_code(d)


def check_verification_code(d):
    print("start checking_verification_code url")
    while True:
        find_code = False
        try:
            content = d.find_element(by=By.ID, value="gs_captcha_f")
            find_code = True
        except selenium.common.exceptions.NoSuchElementException as e:
            pass

        try:
            content = d.find_element(by=By.ID, value="recaptcha")
            find_code = True
        except selenium.common.exceptions.NoSuchElementException as e:
            pass

        if find_code:
            print("Plesse input verification_code")
            time.sleep(2)
        else:
            break
    print("finish checking_verification_code url")


def get_cite_name_list(d):
    text = d.find_element_by_xpath("//*").get_attribute("outerHTML")
    soup = BeautifulSoup(text, "html.parser")
    main_element = soup.find(name="div", attrs={"id": "gs_res_ccl_mid"})
    articles = main_element.find_all(name="div", attrs={"class": "gs_r"})
    cite_name_list = []
    for article in articles:
        name = article.find_all(name="h3", attrs={"class": "gs_rt"})[0].text
        cite_name_list.append(name)     #每一篇引用文章的名字，加入cite_name_list里面
    return cite_name_list









if __name__ == "__main__":
    main()
