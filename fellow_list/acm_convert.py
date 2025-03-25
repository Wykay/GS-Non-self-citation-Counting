#!/usr/bin/env python3

def convert_name_format(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    converted_lines = []
    for line in lines:
        # 将每行以逗号分割
        parts = line.split(',')
        if len(parts) == 2:
            # 去除多余空白字符后交换顺序
            last_name = parts[0].strip()
            first_name = parts[1].strip()
            converted_lines.append(f"{first_name} {last_name}")
        else:
            # 如果格式不符合预期，则原样保留
            converted_lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as f:
        for name in converted_lines:
            f.write(name + "\n")

if __name__ == "__main__":
    convert_name_format("acm_out.txt", "acm_converted.txt")
