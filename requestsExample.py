# -*- coding: utf-8 -*-
# author:Gary
# 第一步，导入需要用到的库
import requests

# 第二步，请求网页内容
url = 'https://gary666.com/'  # 需要请求的网页的链接
html = requests.get(url)  # get方式请求数据
print(html.status_code)  # 查看请求的状态码（200表示请求正常）
html.encoding = html.apparent_encoding  # 设置编码，防止由于编码问题导致文字错乱
print(html.text)  # 查看请求到的内容

# 第三步，解析你需要的内容

# 第四步，存储数据
