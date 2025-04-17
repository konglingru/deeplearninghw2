import spacy


class Reference:
    def __init__(self, number, authors, title):
        self.number = number
        self.authors = authors
        self.title = title

    def __str__(self):
        return f"标号: {self.number}\n作者: {self.authors}\n文献名称: “{self.title}”\n"


# 加载英文语言模型
nlp = spacy.load("en_core_web_sm")

try:
    # 从 test.txt 文件中读取文本内容
    with open('test.txt', 'r', encoding='utf-8') as file:
        text = file.read()
except FileNotFoundError:
    print("未找到 test.txt 文件，请检查文件路径和文件名。")
    exit(1)
except Exception as e:
    print(f"读取文件时出现错误: {e}")
    exit(1)

# 查找 REFERENCES 部分的起始位置
start_index = text.find("REFERENCES")
if start_index == -1:
    print("未找到 REFERENCES 部分。")
    exit(1)

# 提取 REFERENCES 部分之后的文本
references_text = text[start_index + len("REFERENCES"):]

doc = nlp(references_text)
references = []
current_ref = ""
for sent in doc.sents:
    sent_text = sent.text.strip()
    if sent_text.startswith('[') and sent_text[1].isdigit():
        if current_ref:
            references.append(current_ref.strip())
            current_ref = ""
    current_ref += sent_text + " "
if current_ref:
    references.append(current_ref.strip())

reference_objects = []
for ref in references:
    number = ref.split(']')[0].strip('[')
    parts = ref.split('“')
    if len(parts) >= 2:
        authors = parts[0].split('] ')[-1].strip()
        title = parts[1].split('”')[0].strip()
        reference_objects.append(Reference(number, authors, title))

output_file_path = 'references.txt'
try:
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for ref_obj in reference_objects:
            # 仅写入文献名称并换行
            file.write(ref_obj.title + '\n')
    print(f"文献名称已成功保存到 {output_file_path}，每行一个文献")
except Exception as e:
    print(f"保存文件时出现错误: {e}")