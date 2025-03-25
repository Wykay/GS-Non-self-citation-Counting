#本程序基本没用，未作修改，因为爬取的文章里面大多没有以下字符串

#把引用文章列表cite_list里面的[HTML][PDF]等字符串全部去掉，仍然保存在articles.json，并生成未去字符串的备份文件articles.bak.json

from utils import load_json, save_json


def main():
    articles = load_json("data/articles.json")
    save_json(articles, "data/articles.bak.json")    #备份，里面的cite_list没有去标签里的部分词语
    new_articles = articles.copy()                   #包含所有论文及引用该论文的名称列表
    for article_id, article in enumerate(articles):
        if "cite_list" not in article:               #跳过无引用文章
            continue
        cite_articles = article["cite_list"]         #引用文章列表
        for cite_article_id, cite_article in enumerate(cite_articles):   #对每篇引用文章，把标题里面的以下标签全部去掉
            title = cite_article["title"]   #该篇引用文章标题
            clear_contents = [
                "[HTML][HTML] ",
                "[PDF][PDF] ",
                "[BOOK][B] ",
                "[CITATION][C] ",
                "[DOC][DOC] ",
                "[",
            ]
            for clear_content in clear_contents:     #把标题里的上面这些标签全部清除
                title = title.replace(clear_content, "")
            new_articles[article_id]["cite_list"][cite_article_id]["title"] = title
    save_json(new_articles, "data/articles.json")


if __name__ == "__main__":
    main()
