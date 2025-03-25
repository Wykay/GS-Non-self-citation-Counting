# -*- coding: utf-8 -*-
def extract_names(input_file, output_file):
    # 读取整个文件内容
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 按空行分块，每个块代表一个获奖人或一个年份标识
    blocks = content.split("\n\n")
    names = []
    
    for block in blocks:
        # 去除首尾空白字符并分割成行
        lines = block.strip().splitlines()
        if not lines:
            continue

        # 如果第一行以 "Elected in" 开头，则下一行为获奖人信息
        if lines[0].startswith("Elected in"):
            if len(lines) >= 2:
                info_line = lines[1]
            else:
                continue  # 如果没有获奖人信息则跳过
        else:
            info_line = lines[0]
        
        # 提取第一行中逗号之前的内容作为姓名
        name = info_line.split(",")[0].strip()
        if name:
            names.append(name)
    
    # 将所有姓名写入输出文件，每个姓名占一行
    with open(output_file, "w", encoding="utf-8") as f:
        for name in names:
            f.write(name + "\n")

if __name__ == "__main__":
    extract_names("aaai.txt", "aaai_out.txt")
