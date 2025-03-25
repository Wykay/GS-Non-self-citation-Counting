from bs4 import BeautifulSoup

# 读取 iapr.html 文件内容
with open("iapr.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(html_content, "html.parser")

# 查找所有 <strong> 标签，并提取其中的文本（即名字）
names = [tag.get_text(strip=True) for tag in soup.find_all("strong")]

# 将所有名字写入 out.txt，每个名字占一行
with open("iapr_out.txt", "w", encoding="utf-8") as outfile:
    for name in names:
        outfile.write(name + "\n")
