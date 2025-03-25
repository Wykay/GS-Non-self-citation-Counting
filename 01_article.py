#爬取Google Scholar上指定文章的他引次数，并输出由他引论文标题、作者组成的tayin.json文件
#流程：  先按github指示配置config.json里面的scholar_id和 chromedriver.exe在系统的路径
#       删除data文件夹下的 articles_id_0.json 文件
#       再依次执行01_ 02_ 03_ 04_05_06_的py文件，其中02_ ，04_，05_开头需要指定哪篇论文



#爬取作者每篇文章的 ID（序号）、标题 以及 ”引用“接口的网址


from utils import save_json, load_json
import json
from google_scholar import GoogleScholarUser


def fetch():
    config = load_json("config.json")
    user_id = config["scholar_id"]
    scraper = GoogleScholarUser(user_id)
    scraper.get_scholar_articles()      #获取作者所有文章
    articles = scraper.articles

    article_infos = []
    for article_id, article in enumerate(articles):
        info = {                                      #作者每篇文章的信息
            "article_id": article_id,
            "name": article.find_all('a')[0].text,
            "cite_url": article.find_all('a')[1]['href']    #“引用”界面的网址
        }
        article_infos.append(info)
    save_json(article_infos, "data/articles.json")


if __name__ == '__main__':
    fetch()

