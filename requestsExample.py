# -*- coding: utf-8 -*-
# author:Gary
# 第一步，导入需要用到的库
import requests
from bs4 import BeautifulSoup

# 第二步，请求网页内容
url = 'https://gary666.com/'  # 需要请求的网页的链接
html = requests.get(url)  # get方式请求数据
print(html.status_code)  # 查看请求的状态码（200表示请求正常,404内容没有找到）
html.encoding = html.apparent_encoding  # 设置编码，防止由于编码问题导致文字错乱
print(html.text)  # 查看请求到的内容
content = html.text

# 第三步，解析你需要的内容
#html.parser,lxml
soup = BeautifulSoup(content, "html.parser")
# 1 按标签名查找标签
# soup.标签名 # 获取第一个匹配到的标签
print('获取第一个匹配到的超链接', soup.a)  # 获取第一个匹配到的超链接

# 2 属性
# soup.标签名.attrs # 获取标签中所有属性名与对应属性值的字典
print('获取超链接中所有属性名与对应属性值的字典', soup.a.attrs)  # 获取超链接中所有属性名与对应属性值的字典
# soup.标签名.attrs["属性名"]获取属性名对应的属性值
print('获取超链接href属性对应的属性值', soup.a.attrs["href"])  # 获取超链接href属性对应的属性值
# soup.标签名["属性名"]获取属性名对应的属性值的简写
print('获取超链接href属性对应的属性值的简写', soup.a["href"])  # 获取超链接href属性对应的属性值的简写
# soup.标签名.string  # 获取第一个匹配到的标签的内容
print('获取第一个匹配到的超链接的内容', soup.a.string)  # 获取第一个匹配到的超链接的内容
# soup.标签名.text  # 获取第一个匹配到的标签以及其所包含的子标签的所有内容
print('获取第一个匹配到的超链接以及其所包含的子标签的所有内容', soup.a.text)  # 获取第一个匹配到的超链接以及其所包含的子标签的所有内容

# 3 函数
# soup.标签名.get_text()  # 同soup.标签名.text
print(soup.a.get_text())  # 同soup.a.text
# soup.find("标签名") # 同soup.标签名
print(soup.find("a"))  # 同soup.a
print(soup.find("a", href="/detail?dbname=life&num=35"))  # 根据属性值定位到第一个匹配到的标签
# 注意： 若属性名是 class 则需要在后面加个下划线,写成 class_
# soup.find_all("标签名") # 获取匹配到的所有标签, 返回一个列表
a_list = soup.find_all("a")  # 获取所有的超链接
for a in a_list:  # 循环查看每个超链接的文字和url
    if a.string is None:  # 如果超链接的内容为空
        continue
    else:
        print(a.string + ":" + a.get("href"))
# soup.find_all(["标签1", "标签2"])   可以获取多种类的标签，通过列表指定获取的多个标签
soup.find_all(["a", "div"])  # 可以获取多种类的标签，通过列表指定获取的多个标签
# soup.find_all("标签名", limit=int(n))  # limit参数指定获取个数，为整数
print(soup.find_all("a", limit=2))  # 获取前2个匹配到的超链接

# 第四步，存储数据
