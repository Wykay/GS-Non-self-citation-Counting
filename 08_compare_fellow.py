from utils import load_txt

def main():
    num = 0  #统计IEEE FELLOW数
    current_dict = load_txt("other-cite/HCP(472).txt")      #自引过滤后的

    ieee_fellow = load_txt("fellow/IEEE fellow list new.txt")


    for item in current_dict:
        author = item
        print(item)
        for fellow in ieee_fellow:
#            print(fellow)
            if author == fellow:
                num+=1

    print(num)

if __name__ == "__main__":
    main()
