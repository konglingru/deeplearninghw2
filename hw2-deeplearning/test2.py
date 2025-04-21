import re


class Reference:
    def __init__(self, number, title):
        self.number = number
        self.title = title

    def __str__(self):
        return f"标号: {self.number}\n文献名称: {self.title}\n"


try:
    with open('test.txt', 'r', encoding='utf-8') as file:
        text = file.read()
except FileNotFoundError:
    print("未找到 test.txt 文件，请检查文件路径和文件名。")
    exit(1)
except Exception as e:
    print(f"读取文件时出现错误: {e}")
    exit(1)

start_index = text.find("References")
if start_index == -1:
    print("未找到 References 部分。")
    exit(1)

references_text = text[start_index + len("References"):]

# 定义正则表达式，匹配标号、标题（在第一个.和第二个.之间）
pattern = r'\[(\d+)\](.*?)\.(.*?)\.'
matches = re.findall(pattern, references_text, re.DOTALL)

reference_objects = []
for match in matches:
    number = f"[{match[0]}]"
    # 提取标题内容，去除换行符并去掉首尾空格
    title = match[2].replace('\n', ' ').strip()
    reference_objects.append(Reference(number, title))

output_file_path = 'references.txt'
try:
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for ref_obj in reference_objects:
            file.write(f"{ref_obj.number} {ref_obj.title}\n")
    print(f"文献标号和标题已成功保存到 {output_file_path}，每行格式为“[标号] 标题”")
except Exception as e:
    print(f"保存文件时出现错误: {e}")
    