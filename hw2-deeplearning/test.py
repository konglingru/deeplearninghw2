import spacy


class Reference:
    def __init__(self, number, title):
        self.number = number
        self.title = title

    def __str__(self):
        return f"标号: {self.number}\n文献名称: {self.title}\n"


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
start_index = text.find("References")
if start_index == -1:
    print("未找到 REFERENCES 部分。")
    exit(1)

# 提取 REFERENCES 部分之后的文本
references_text = text[start_index + len("References"):]

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
    # 提取标号（保留方括号格式）
    number = ref.split(']')[0].strip() + ']'
    # 去除标号部分
    ref_content = ref[len(number):].strip()
    # 查找作者信息结束的第一个句号
    author_end = ref_content.find('.')
    if author_end != -1:
        # 提取标题，标题在作者信息后的第一个句号之后
        title = ref_content[author_end + 1:].strip()
        # 去除标题后面可能跟着的会议信息等内容，以 "In " 为分隔
        in_index = title.find('In ')
        if in_index != -1:
            title = title[:in_index].strip()
        reference_objects.append(Reference(number, title))

output_file_path = 'references.txt'
try:
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for ref_obj in reference_objects:
            # 写入格式：[标号] 标题（每行一个）
            file.write(f"{ref_obj.number} {ref_obj.title}\n")
    print(f"文献标号和标题已成功保存到 {output_file_path}，每行格式为“[标号] 标题”")
except Exception as e:
    print(f"保存文件时出现错误: {e}")
    