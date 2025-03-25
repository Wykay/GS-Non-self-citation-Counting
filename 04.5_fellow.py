import os

# 读取各个 Fellow 列表
with open('./fellow_list/ieee_final.txt', 'r', encoding='utf-8') as f:
    ieee_fellows = set(line.strip() for line in f.readlines())
with open('./fellow_list/acm_final.txt', 'r', encoding='utf-8') as f:
    acm_fellows = set(line.strip() for line in f.readlines())
with open('./fellow_list/iapr_final.txt', 'r', encoding='utf-8') as f:
    iapr_fellows = set(line.strip() for line in f.readlines())
with open('./fellow_list/aaai_final.txt', 'r', encoding='utf-8') as f:
    aaai_fellows = set(line.strip() for line in f.readlines())
with open('./fellow_list/fellow_name_list.txt', 'r', encoding='utf-8') as f: #多一个list来源，防止遗漏
    other_fellows = set(line.strip() for line in f.readlines())

# 定义输入与输出文件夹路径
input_folder = './paper/all_citation'
output_folder = './paper/fellow'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历输入文件夹中的每个 txt 文件
for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        input_file_path = os.path.join(input_folder, filename)
        output_file_path = os.path.join(output_folder, filename)
        
        # 读取论文信息
        with open(input_file_path, 'r', encoding='utf-8') as f:
            papers = f.readlines()
        
        with open(output_file_path, 'w', encoding='utf-8') as out_file:
            for paper in papers:
                paper_info = paper.strip()
                # 假设作者信息位于第一个句号之前
                authors = paper_info.split('.')[0]
                author_list = [author.strip() for author in authors.split(',')]
                
                # 分别查找各个 Fellow 类别
                ieee_authors = [author for author in author_list if author in ieee_fellows]
                acm_authors = [author for author in author_list if author in acm_fellows]
                iapr_authors = [author for author in author_list if author in iapr_fellows]
                aaai_authors = [author for author in author_list if author in aaai_fellows]
                other_authors = [author for author in author_list if author in other_fellows]
                
                # 只有至少存在一类 Fellow 时才输出该论文及对应信息
                if ieee_authors or acm_authors or iapr_authors or aaai_authors or other_authors:
                    out_file.write(paper)
                    out_file.write("IEEE Fellow: " + (", ".join(ieee_authors) if ieee_authors else "None") + "\n")
                    out_file.write("ACM Fellow: " + (", ".join(acm_authors) if acm_authors else "None") + "\n")
                    out_file.write("IAPR Fellow: " + (", ".join(iapr_authors) if iapr_authors else "None") + "\n")
                    out_file.write("AAAI Fellow: " + (", ".join(aaai_authors) if aaai_authors else "None") + "\n")
                    out_file.write("other Fellow: " + (", ".join(other_authors) if other_authors else "None") + "\n\n")
        
        print(f"处理完成，结果已保存到 {output_file_path}")

print("所有文件处理完成！")

