import fitz
import re
import sys


class ReferenceExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text = self.extract_text_from_pdf()

    def extract_text_from_pdf(self):
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

    def find_references(self):
        # 假设参考文献部分以 "References" 开头
        start_index = self.text.find("REFERENCES")
        if start_index == -1:
            print("References section not found.")
            return []
        references_text = self.text[start_index + len("REFERENCES"):]
        # 调整后的正则表达式
        pattern = r'^\[(\d+)\]\s+(.*?)(?=\n\[\d+\]\s+|$)'
        matches = re.findall(pattern, references_text, re.M | re.S)
        return [ref[1].strip() for ref in matches]


if __name__ == "__main__":
    pdf_path = 'C://Users//14016//Desktop//hw2-deeplearning//example2.pdf'
    extractor = ReferenceExtractor(pdf_path)
    references = extractor.find_references()
    sys.stdout.reconfigure(encoding='utf-8')
    for idx, ref in enumerate(references, start=1):
        print(f"{idx}. {ref}")