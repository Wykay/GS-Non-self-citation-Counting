from utils import load_txt

def main():
    num = 0  #统计IEEE FELLOW数
    current_dict = load_txt("other-cite/HCP(472).txt")      #自引过滤后的

    ieee_fellow = load_txt("D:/yuxiao/File/code/avvp/GS-Non-self-citation-Counting-main/GS-Non-self-citation-Counting-main/fellow_list/ieee_final.txt")


    for item in current_dict:
        author = item
        print(item)
        for fellow in ieee_fellow:
#            print(fellow)
            if author == fellow:
                num+=1

    print(num)

    # # 打开一个文件用于写入，设置编码为 utf-8
    # with open("./paper/2Layer-Specific.txt", "w", encoding="utf-8") as file:
    #     for item in current_dict:
    #         author = item
    #         # 将 item 写入文件，同时换行
    #         print(item, file=file)
    #         for fellow in ieee_fellow:
    #             if author == fellow:
    #                 num += 1

    #     # 将计数结果写入文件
    #     print(num, file=file)


if __name__ == "__main__":
    main()
