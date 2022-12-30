#把包含了引用文章作者列表的信息。保存到articles_id_{parallel_id}.json里面

#本程序主要：
#   排除他引并统计：总引用次数 自引次数 他引次数 输出他引文章的信息列表，以上四项保存到result/result.txt中

# tayin.json保存了所有他引文章
# 命令行打印他引和自引次数
# 保存引用信息到result/result.txt中

#**********指定参数：
target_id = 50    #要爬取google scholar 主页上的第几篇

from utils import load_json, save_json
from pathlib import Path
from bs4 import BeautifulSoup
import time
import requests
import sys
import json
import os

DBLP_BASE_URL = 'http://dblp.uni-trier.de/'
PUB_SEARCH_URL = DBLP_BASE_URL + "search/publ/"


def main():


#调试
    parallel_id = 0      #0~parallel_count之间的数，每parallel_count篇文章才执行爬取引用的作者列表
    parallel_count = 8   #作者推荐是8



    save_path = Path("data/articles_id_{}.json".format(parallel_id))
    if not save_path.exists():
        base_path = Path("data/articles.json")     #base_path里面有去了标签的引用列表
    else:
        base_path = save_path


    articles = load_json(base_path)
    new_articles = articles.copy()

    for article_id, article in enumerate(articles):    #对作者的每篇paper

        #-----------只爬取所有引用第target_id篇论文的文章的作者列表--------
        if article_id != target_id:          #这里可以指定爬取哪篇文章
            continue


        current_authors,current_year,current_publisher = query(new_articles[article_id]["name"])       #目标文章的发表信息
        print("本文作者：",current_authors)

        if "cite_list" not in article:                 #无引用则跳过
            continue


        cite_articles = article["cite_list"]
        for cite_article_id, cite_article in enumerate(cite_articles):  #每篇引用的文章
            if "author" in cite_article:       #如果有作者列表了，就跳过（但是一般都没有，原作者是通过下面query函数找）
                continue
            title = cite_article["title"]
            while True:
                try:
                                                              #这里有个问题：对于比较新的文章，如2022年的paper，可能会查询不到year,publisher
                    authors,year,publisher = query(title)     #根据引用文章标题，查询作者 发表时间 发表位置
                    break
                except Exception as e:
                    print(e)
                    time.sleep(1)

            if authors == -1 or year == -1 or publisher == -1:                                             #查找失败情况，跳过该篇，文件中表示查找不到
                authors = {}
                year = 'search fail'
                publisher = 'search fail'
            print("{}/{} {} {}".format(cite_article_id, len(cite_articles), title, " ".join(authors)))


            new_articles[article_id]["cite_list"][cite_article_id]["author"] = authors                   #加入了作者信息，authors为list型

            new_articles[article_id]["cite_list"][cite_article_id]["year"] = year                        #加入了年份信息
            new_articles[article_id]["cite_list"][cite_article_id]["publisher"] = publisher              #加入了发表位置信息

            save_json(new_articles, save_path)    #把包含了引用文章作者列表的信息，保存到articles_id_{}.json里面


#此处with open 后已经获得目标文章的被引用列表（文章标题+作者），进行自引删除和他引统计，他引次数会打印出来，他引文章会保存到tayin.json
        with open('data/target.json','w') as f:   #记录作者名单
            json.dump(new_articles[article_id]["cite_list"],f)      #写下该文章的cite_list：引用文章名称及作者

            ziyin_times = 0  # 自引次数
            tayin=[]         # 他引列表

            #下一步开发：将target.json中的自引词条去掉，并统计剩余的他引次数
            #检查是否自引，若是则删除该词条   和current_authors做对比
            for item in new_articles[article_id]["cite_list"] :       #item包含了title 和 author
                # print(item["author"])
                isziyin = 0  # 是否自引


                for author in item["author"]:           #是否自引的判断
                #     print(author,end=' ')
                # print("\n")
                    if author in current_authors:         #自引
                        isziyin = 1
                        ziyin_times += 1
                        break
                    else:
                        continue

                if isziyin == 0:            #记录他引
                    tayin.append(item)

            with open('data/tayin.json','w') as file:                            #保存他引
                json.dump(tayin,file)
            print('tayin.json文件内列表的长度：',len(tayin))

            #统计最后剩余的 他引次数
            print('总计引用',len(new_articles[article_id]["cite_list"]))
            print('自引次数：', ziyin_times)
            print('他引次数：',len(new_articles[article_id]["cite_list"])-ziyin_times )

            write_to_txt(len(new_articles[article_id]["cite_list"]),
                         ziyin_times,
                         len(new_articles[article_id]["cite_list"])-ziyin_times)

#通过文章标题title查找作者列表author year,publisher 依次为：列表，字符串，字符串
def query(title):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0',
        'Cookie': 'GSP=CF=4'
    }
    resp = requests.get(PUB_SEARCH_URL, headers=headers, params={'q': [title]})
    time.sleep(1)
    d = BeautifulSoup(resp.content, "html.parser")
    # d = BeautifulSoup(open('D://b.html',encoding='utf-8'),features='html.parser')
    pub_list_raw = d.find(name="ul", attrs={"class": "publ-list"})      #找到包含发布信息的子树

    # #找到span class="Z3988"里面的title字符串，内包含标题、发表位置、年份等
    # pub_year_raw = d.find(name="span",attrs={"class": "Z3988"})         #找到包含发布年份、发布者的子串
    # sub_title = pub_year_raw["title"]            #字符串，内部  rft.btitle=期刊名字 	rft.date=年份

    #爬取年份和发布位置
        # find_all( name , attrs , recursive , string , **kwargs )
    #年份
    year_item = d.find(name="span",attrs={"itemprop": "datePublished"})         #年份对应子树  find 返回 tag
    print(type(year_item))
    if year_item is None :           #对于最新的文章，可能检索不到年份和发表位置，直接返回
        return -1,-1,-1
    else:
        year = str(year_item.get_text())         #此处爬取得到发表年份，string类型
        #发布位置
            #<span itemprop="name">  子树有多个个，最后一个对应Publisher的item
        publisher_item = d.findAll(name="span",attrs={"itemprop": "name"})
        publisher = str(publisher_item[-1].get_text())   #string 类型

        #爬取该文章的作者列表
        authors = []
        for pub_data in pub_list_raw.children:
            if pub_data.attrs.get('class')[0] == 'year':
                continue
            author_items = pub_data.findAll(name="span", attrs={"itemprop": "author"})
            for author_item in author_items:
                authors.append(author_item.text)
            break
        return authors,year,publisher

#按照引用格式，把他引写入到txt文件中
def write_to_txt(zongyin,ziyin,tayin):   #,authors   ,title    ,publisher    ,year
    txt_path = 'result/result.txt'
    file = open(txt_path,mode='w',encoding='utf-8')                   #用utf-8编码，防止一些作者名字不能写入txt（默认gbk）

#write参数必须为str
    file.write("总引用次数：")
    file.write(str(zongyin))
    file.write(" 自引次数：")
    file.write(str(ziyin))
    file.write(" 他引次数：")
    file.write(str(tayin))
    file.write("\n\n")

#把tayin.jason中的信息写到result.txt中

    with open('data/tayin.json', encoding='utf-8') as fh:
        file_tayin = json.load(fh)

    for id, item in enumerate(file_tayin):
        author_num = len(item["author"])
        #文章作者
        i = 0
        for author in item["author"] :
            file.write(author)
            #最后一个作者后面要是句号.
            if i < author_num-1 :
                file.write(',')
                i+=1
            else:
                file.write('.')
        #文章标题
        file.write(' ')
        file.write(str(item["title"]))
        #文章发表位置
        file.write('. ')
        file.write(str(item["publisher"]))
        #文章发表年份
        file.write(', ')
        file.write(str(item["year"]))

        file.write("\n")

    file.close()



if __name__ == "__main__":
    main()