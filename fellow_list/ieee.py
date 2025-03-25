#!/usr/bin/env python3

def extract_fellow_names(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        # 去掉空行，并去除两侧空白字符
        lines = [line.strip() for line in f if line.strip()]
    
    # 过滤掉包含页码及"IEEE Fellows Class"的行
    filtered_lines = [line for line in lines if "IEEE Fellows Class" not in line]
    
    # 每个fellow的记录由四行构成，第一行为名字
    names = [filtered_lines[i] for i in range(0, len(filtered_lines), 4)]
    
    with open(output_file, "w", encoding="utf-8") as f:
        for name in names:
            f.write(name + "\n")

if __name__ == "__main__":
    extract_fellow_names("ieee.txt", "ieee_out.txt")
