# -*- coding: utf-8 -*-
# author:Gary
# 第一步，导入需要用到的库
import requests
from bs4 import BeautifulSoup

# 根据需要引入存储数据的库
import pymysql

import time  # 设置爬取时间间隔，防止访问过快ip被封等

# 第二步，请求网页内容
url = 'https://gary666.com/learn'  # 需要请求的网页的链接
html = requests.get(url)  # get方式请求数据
# print(html.status_code)  # 查看请求的状态码（200表示请求正常,404内容没有找到）
html.encoding = html.apparent_encoding  # 设置编码，防止由于编码问题导致文字错乱
# print(html.text)  # 查看请求到的内容
html_content = html.text

# 第三步，解析你需要的内容
# html.parser,lxml
soup = BeautifulSoup(html_content, "html.parser")
all_div = soup.find_all("div", class_="blogs")  # 观察发现所有的内容都在class为blogs的div中，所以直接定位
# print(all_div)
data_list = []  # 存储所有数据，供存储使用
for div in all_div:  # 循环查看每个超链接的文字和url
    if div is None:  # 如果div的内容为空
        continue
    else:
        title = div.find('h3').find('a').text  # 文章标题
        content = div.find('p').text  # 文章内容
        author = div.find('li', class_='author').text  # 作者
        t_type = div.find('li', class_='lmname').text  # 文章分类
        timer = div.find('li', class_='timer').text  # 时间
        single_blog = (title, content, author, t_type, timer)  # 单个blog内容
        data_list.append(single_blog)  # 添加到所有的数据中去
        print(title, content, author, t_type, timer)


#  选做内容

# 第四步，存储数据
def insert_data(datalist):
    # 连接数据库，主机名默认本地，端口默认3306，用户名默认root，字符集默认utf-8，需要传入数据库密码和数据库名
    # 你的密码password参数，数据库名db参数，下面示例密码是your_password,数据库名是spider(需要自己先建立好数据库表)
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='Xts0916.', db='spider',
                           charset='utf8')  # 连接数据库
    cur = conn.cursor()  # 用于访问和操作数据库中的数据（一个游标，像一个指针）
    # 示例是spider中建立了blog表，然后表的属性有title, content, author, t_type, timer，正常运行先需要建立好
    # content的数据类型建议设为text
    sql = 'insert into blog(title, content, author, t_type, timer) values(%s,%s,%s,%s,%s)'  # 插入多条
    cur.executemany(sql, datalist)  # data_list类型是列表中嵌套多个元组比如[(),(),()]
    conn.commit()  # 提交事务,执行了这一步数据才真正存到数据库
    '''
    如果需要单条插入放入到上面循环的36行后执行即可 
    sql='insert into blog(title, content, author, t_type, timer) values("{}","{}","{}",
    "{}","{}")'.format(title, content, author, t_type, timer)#插入单条 cur.execute(sql) 
    '''
    cur.close()  # 关闭游标
    conn.close()  # 关闭数据库连接


# 执行插入数据函数
# print(data_list)
# insert_data(data_list)

# 爬取多页(爬取其他页面数据)
def many_page(page):
    # 设置头部信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    # url = 'https://gary666.com/learn?page=2'  # 通过观察发现是否page控制的翻页，page=几就是第几页
    # 方法一，直接修改url（参数不多推荐这个）
    single_url = 'https://gary666.com/learn?page={}'.format(page)
    res = requests.get(single_url, headers=headers)  # 获取网页内容
    # 方法二，构造参数,通过参数
    '''
    params = {'page':page}
    res=requests.get(url='https://gary666.com/learn',params=params,headers=headers)#获取网页内容
    '''
    res.encoding = res.apparent_encoding  # 设置编码
    if res.status_code == 200:  # 如果状态码为200则正常
        return res.text  # 返回网页内容
    else:
        print('爬取网页异常')


# 通过bs4解析网页内容
def ana_html(html):
    soup = BeautifulSoup(html, "html.parser")
    all_div = soup.find_all("div", class_="blogs")  # 观察发现所有的内容都在class为blogs的div中，所以直接定位
    # print(all_div)
    data_list = []  # 存储所有数据，供存储使用
    for div in all_div:  # 循环查看每个超链接的文字和url
        if div is None:  # 如果div的内容为空
            continue
        else:
            title = div.find('h3').find('a').text  # 文章标题
            content = div.find('p').text  # 文章内容
            author = div.find('li', class_='author').text  # 作者
            t_type = div.find('li', class_='lmname').text  # 文章分类
            timer = div.find('li', class_='timer').text  # 时间
            single_blog = (title, content, author, t_type, timer)  # 单个blog内容
            data_list.append(single_blog)  # 添加到所有的数据中去
            print(title, content, author, t_type, timer)
    return data_list  # 返回数据列表


if __name__ == '__main__':
    for page in range(1, 9):  # range的范围就是页数的范围
        print('正在爬取第{}页'.format(page))
        html = many_page(page)  # 获取网页内容
        data_list = ana_html(html)  # 解析需要的内容
        time.sleep(0.5)  # 每爬取一次停止0.5s在继续爬取
        insert_data(data_list)  # 存储数据
    print('爬取完成!')
