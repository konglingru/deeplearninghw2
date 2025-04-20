import re


def extract_titles(text):
    title_pattern = re.compile(r'^\[\d+\]\s.*?\.\s(.*?)\.\sIn', re.MULTILINE | re.DOTALL)
    titles = title_pattern.findall(text)
    return titles


text = """
[32] Ze Liu, Han Hu, Yutong Lin, Zhuliang Yao, Zhenda Xie,
Yixuan Wei, Jia Ning, Yue Cao, Zheng Zhang, Li Dong, et al.
Swin transformer v2: Scaling up capacity and resolution. In
CVPR, pages 12009–12019, 2022. 7, 8
[33] Matthew Loper, Naureen Mahmood, Javier Romero, Gerard
Pons-Moll, and Michael J Black. Smpl: A skinned multi-
person linear model. ACM ToG, 34(6), 2015. 3
[34] Xiaoxuan Ma, Jiajun Su, Chunyu Wang, Wentao Zhu, and
Yizhou Wang. 3d human mesh estimation from virtual mark-
ers. In CVPR, pages 534–543, 2023. 3
[35] Naureen Mahmood, Nima Ghorbani, Nikolaus F. Troje, Ger-
ard Pons-Moll, and Michael J. Black. Amass: Archive of
motion capture as surface shapes. In ICCV, 2019. 5
"""

titles = extract_titles(text)
for title in titles:
    print(title.replace('\n', ' ').strip())

    