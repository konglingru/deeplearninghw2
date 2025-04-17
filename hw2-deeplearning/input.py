import fitz
import sys


def extract_text_pymupdf(pdf_path):
    text = ""
    try:
        pdf_document = fitz.open(pdf_path)
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        pdf_document.close()
    except Exception as e:
        print(f"读取 PDF 时出错: {e}")
    return text


# 替换为你的论文 PDF 文件路径
pdf_path = 'example2.pdf'
extracted_text = extract_text_pymupdf(pdf_path)
sys.stdout.reconfigure(encoding='utf-8')

output_file_path = 'test.txt'
try:
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(extracted_text)
    print(f"提取的文本已保存到 {output_file_path}")
except Exception as e:
    print(f"保存文件时出错: {e}")