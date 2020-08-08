# -*- coding: utf-8 -*-
# author:Gary
import requests

url = 'https://www.gary666.com/result'  # 需要post的url
for page in range(1, 33):  # 多少页
    data = {
        'page': page,
        'rows': 10
    }  # 需要post的数据
    res = requests.post(url, data).json()  # 获取post的返回数据，也可以采用.text方法获取网页内容
    print(res)  # 查看返回内容
    items = res['rows']  # 提取主要内容
    for item in items:  # 获取对应的信息
        print(item['Cname'], item['grade'], item['Tname'], item['department'], item['type'], item['timeLocation'],
              item['tips'])
