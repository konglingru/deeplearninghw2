import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
from bs4 import XMLParsedAsHTMLWarning
import warnings

# 过滤 XML 解析警告
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

def extract_title(line):
    """从带标号的行中提取纯标题（如将 [1] 标题内容 转为 标题内容）"""
    return re.sub(r'^\[\d+\]\s*', '', line.strip())  # 去除开头的 [数字] 标号

def get_bib_url_from_dblp(title):
    """从 DBLP 获取 BibTeX 链接（使用纯标题搜索）"""
    base_url = "https://dblp.org/search/publ/api"
    params = {
        "q": title,       # 纯标题搜索
        "h": 1,
        "format": "xml"   # 使用 XML 格式响应
    }
    search_url = base_url + "?" + urllib.parse.urlencode(params)
    
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, features="xml")  # 明确使用 XML 解析器
        
        hit = soup.find('hits').find('hit')
        if hit:
            publ_url = hit.find('info').find('url').text
            return publ_url + ".bib"
        print(f"DBLP未找到: {title}")
        return None
    except Exception as e:
        print(f"DBLP请求错误: {e}")
        return None

def get_bib_url_from_arxiv(title):
    """从 arXiv 获取 BibTeX 链接（使用纯标题搜索）"""
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"ti:{title}",  # 在标题字段搜索
        "start": 0,
        "max_results": 1
    }
    search_url = base_url + "?" + urllib.parse.urlencode(params)
    
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, features="xml")
        
        entry = soup.find('entry')
        if entry:
            arxiv_id = entry.find('id').text.split('/')[-1]
            return f"https://arxiv.org/bibtex/{arxiv_id}"
        print(f"arXiv未找到: {title}")
        return None
    except Exception as e:
        print(f"arXiv请求错误: {e}")
        return None

def download_bib_file(bib_url, file_path):
    """下载并保存 BibTeX 文件（使用 UTF-8 编码）"""
    if bib_url:
        try:
            response = requests.get(bib_url)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"成功保存: {file_path}")
        except Exception as e:
            print(f"下载失败: {e}")

if __name__ == "__main__":
    try:
        # 读取带标号的标题文件（每行格式：[标号] 标题内容）
        with open('references.txt', 'r', encoding='utf-8') as f:
            titled_lines = [line for line in f if line.strip()]  # 过滤空行
        
        for idx, line in enumerate(titled_lines, 1):
            pure_title = extract_title(line)  # 提取纯标题
            bib_url = get_bib_url_from_dblp(pure_title)
            
            if not bib_url:
                bib_url = get_bib_url_from_arxiv(pure_title)
            
            file_path = f"downloaded_{idx}.bib"
            download_bib_file(bib_url, file_path)

    except FileNotFoundError:
        print("错误：未找到 references.txt 文件")
    except Exception as e:
        print(f"程序异常：{e}")