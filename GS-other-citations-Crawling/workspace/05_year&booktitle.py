#对作者的每篇文章：爬取引用该文章的所有文章的标题，保存在articles.json里面

#注意：因为google用户在本机只能同时登录一个，所以请关闭所有google浏览器窗口

#**********指定参数：
target_id = 4   #要爬取google scholar 主页上的第几篇(从0开始）


import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By        #按照各种元素如ID NAME CSS_SELECTOR定位元素
from bs4 import BeautifulSoup         #爬取数据的库
import time
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
#        base_url = "https://scholar.google.com/scholar?cites=11697193779087888535&as_sdt=2005&sciodt=0,5&hl=en"        #可以直接给引用界面网址
        get_all_cite_name_list(d, base_url)
        print('爬取完成')

#单位：目标文章             爬取名字 年份 发表位置
def get_all_cite_name_list(d, base_url):
    all_list = []

    for start in range(0, 100000, 10):       #从引用页面第几页（从0开始记）*10开始   有时一篇文章引用过多，需要份几次来爬，记得改开始页号
        print("Page {}".format(start // 10))
        url = get_specify_url(base_url, start)    #每一页引用文章列表的网址，数字按10递增，因为每页显示10篇引用文章
        enter_url(d, url)                         #打开该页                           *******引用文章列表的一页
        #time.sleep(10)
        #单位：某一页引用
        cite_name_list = get_cite_name_list(d)    #获取该页的引用文章的：标题列表
            #无引用了则停止爬取
        if len(cite_name_list) == 0:
            break
        info_of_per_page = get_page_yearANDbooktitle(d,url)    #获取该页引用文章的：年份列表，发表位置列表               #多了个url


        #将该页引用文章的：标题 年份 发表位置 插入各自对应的总列表
        all_list.append(info_of_per_page)

        save_json(all_list, "data/cite_info.json")     #保存了作者每篇文章的引用列表（标题，年份，发表位置）
                                                          #之所以还要保留其他未爬取引用列表的作者文章，是为了直接调用原作者写的作者查询程序



def open_browser():         #打开浏览器
    # 我们将本机自带chrome的默认设置导入到webdriver里面
    options = webdriver.ChromeOptions()
    options.add_argument(r"--user-data-dir=C:\Users\10025\AppData\Local\Google\Chrome\User Data")  # e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
    options.add_argument(r'--profile-directory=Profile 1')  # e.g. google用户对应的文件夹，google浏览器对每一个用户都会建立一个文件夹，内含所有设定，书签等等
    print("start openning browser")
    config = load_json("config.json")
    d = webdriver.Chrome(executable_path=config["driver_path"], chrome_options=options)   #获取默认设置
    # d = webdriver.Chrome(executable_path=config["driver_path"])   #获取默认设置
    d.set_window_size(1400, 800)
   # print("finish openning browser")
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

# 人机验证检测代码
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

        try:
            content = d.find_element(by=By.ID, value="infoDiv")
            find_code = True
        except selenium.common.exceptions.NoSuchElementException as e:
            pass

        try:
            content = d.find_element(by=By.XPATH, value="/html/body/div/div//input[@name = 'continue']")
            find_code = True
        except selenium.common.exceptions.NoSuchElementException as e:
            pass

        if find_code:
            print("Plesse input verification_code")
            time.sleep(10)                                #给10s进行人机验证！！！！！！！   牛逼作者！！！！！！！！！！！！
        else:
            break
    print("finish checking_verification_code url")

#获取某页引用文章的所有标题 组成的列表
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

#爬取某页引用文章的 年份列表 以及 发表位置列表
#   每篇引用文章：
#       点击cite-点击BibTeX-判断是inproceceedings还是article：
#           article:爬取 journal 和 year
#           inproceceedings:爬取 booktitle 和 year
def get_page_yearANDbooktitle(d,url):                 #把该页所有引用文章的BibTeX全部爬取

    info = []

    #读取每一篇paper的BibTeX
    #点击import to bibtex按钮，此处单位为：页     每一页有10篇paper
    length = len(d.find_elements_by_xpath("/html/body/div/div//a[@class = 'gs_nta gs_nph']") )   #本页面所有的bibtex按钮的 个数
    #对于每一个bib按钮，对应于本页面的每一篇引用文章

    #跑到最后一页时可能会报错（最后一页没有10个引用），但是没关系，所有数据都保存好了
    for i in range(0, length):
    # for i in range(0,len(d.find_elements_by_xpath("/html/body/div/div//a[@class = 'gs_nta gs_nph']"))):
        bib_buttons = d.find_elements_by_xpath("/html/body/div/div//a[@class = 'gs_nta gs_nph']")  # 本页面所有的bibtex按钮的 url链接
        bib_buttons[i].click()
        #单位：每篇paper:爬取 author,title,booktitle,year
        # time.sleep(3)
        #time.sleep(20)   #每20s爬一次，不然谷歌会频繁弹出人机验证码，若多次验证失败，会封IP
        info.append(d.find_element_by_tag_name('body').text)

        # info.append(d.find_elements_by_xpath("body[@class='name']").text)

        #回到上一页
        enter_url(d, url)

    return info





if __name__ == "__main__":
    main()
