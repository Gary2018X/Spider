# -*- coding: utf-8 -*-
# author:Gary
# 第一步，导入需要用到的库
import requests
from lxml import etree

res = requests.get('https://www.gary666.com/learn')  # 获取网页内容
res.encoding = res.apparent_encoding  # 设置编码，防止由于编码问题导致文字错乱
# 利用 etree.HTML 把字符串解析成 HTML 文件
# res.text就是获取把网页内容转为字符串
html = etree.HTML(res.text)

# 获取某个标签的内容
# 绝对路径定位：
title = html.xpath('/html/body/div[2]/div[1]/div[1]/h3/a')  # 通过调用xpath这个方法就可以获取到对应路径的内容，返回一个列表，需要通过循环输出
for i in title:
    print(i.text)  # .text输出文本内容

# 获取某个标签的属性的值
title1 = html.xpath('/html/body/div[2]/div[1]/div[1]/h3/a/text()')[0]  # 直接通过text()方法获取文本
print(title1)
title_href = html.xpath('/html/body/div[2]/div[1]/div[1]/h3/a/@href')[0]  # 通过/@属性名即可获取对应的属性值
print(title_href)
# 获取指定标签对应属性值的内容
title2 = html_data = html.xpath('/html/body/div[2]/div[1]/div[1]/h3/a[@href="/detail?dbname=study&num=38"]/text()')[0]
print(title2)
