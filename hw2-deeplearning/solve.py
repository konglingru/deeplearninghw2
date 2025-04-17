import requests
from bs4 import BeautifulSoup
import urllib.parse


def get_bib_url_from_dblp(title):
    # 构建搜索 URL
    base_url = "https://dblp.org/search/publ/api"
    params = {
        "q": title,
        "h": 1,
        "format": "lxml"  # 这里应该是 xml 格式，而不是 lxml
    }
    search_url = base_url + "?" + urllib.parse.urlencode(params)

    try:
        # 发送请求获取搜索结果
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        # 提取第一个搜索结果的 URL
        result = soup.find('hits').find('hit')
        if result:
            publ_url = result.find('info').find('url').text
            bib_url = publ_url + ".bib"
            return bib_url
        else:
            print(f"未找到与 '{title}' 相关的文献。")
            return None
    except requests.RequestException as e:
        print(f"请求出错: {e}")
        return None


def download_bib_file(bib_url, file_path):
    if bib_url:
        try:
            # 发送请求下载 BIB 文件
            response = requests.get(bib_url)
            response.raise_for_status()
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f"BIB 文件已下载到 {file_path}")
        except requests.RequestException as e:
            print(f"下载 BIB 文件时出错: {e}")


if __name__ == "__main__":
    try:
        # 从 refexample.txt 文件中读取文献名称
        with open('references.txt', 'r', encoding='utf-8') as file:
            titles = file.readlines()

        for index, title in enumerate(titles, start=1):
            title = title.strip()  # 去除首尾的空白字符
            if title:
                bib_url = get_bib_url_from_dblp(title)
                file_path = f"downloaded_{index}.bib"
                download_bib_file(bib_url, file_path)
    except FileNotFoundError:
        print("未找到 refexample.txt 文件，请检查文件路径和文件名。")
    except Exception as e:
        print(f"发生未知错误: {e}")
