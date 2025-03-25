# 打开 acm.txt 文件并读取所有行
with open("acm.txt", "r", encoding="utf-8") as infile:
    lines = infile.readlines()

# 打开 out.txt 文件准备写入
with open("acm_out.txt", "w", encoding="utf-8") as outfile:
    # 对于每一行，提取 "ACM Fellows" 之前的部分（即名字）
    for line in lines:
        if "ACM Fellows" in line:
            name, _, _ = line.partition("ACM Fellows")
            # 去除多余的空白字符，并写入文件
            outfile.write(name.strip() + "\n")
