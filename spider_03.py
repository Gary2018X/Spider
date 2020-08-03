import time

import requests
from bs4 import BeautifulSoup
from data_admin import database
# 初始化并连接数据库，主机名默认本地，端口默认3306，用户名默认root，字符集默认utf-8，需要传入数据库密码和数据库名
Data_admin = database(password='Z!20010705!ZB', db='douban')

# 传入url参数，返回爬取到的网页
def get_soup(url = 'https://book.douban.com/top250?start=0'):
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36'}
    html = requests.get(url,headers=header)  # get方式请求数据
    # print(html.status_code)  # 查看请求的状态码（200表示请求正常）
    html.encoding = html.apparent_encoding  # 设置编码，防止由于编码问题导致文字错乱
    # print(html.text)  # 查看请求到的内容
    content = html.text
    soup = BeautifulSoup(content, "lxml")
    return soup

#传入网页内容，对其进行进一步的划分获取到想要的内容
def get_htmltext(i,soup):
    j = 1
    tr = soup.find_all("tr",class_='item')  # 获取所有的div
    for a in tr:
        img_href = a.find("a",class_='nbg').find("img").attrs["src"]  # 获取图片链接
        book_name = a.find("div",class_='pl2').find('a').attrs["title"]
        # 获取包括作者、出版社、出版日期、价格等的信息
        b = a.find("p",class_='pl').string.split(" / ")
        price = b[-1]
        date = b[-2]
        publisher = b[-3]
        # 从尾部开始剥离价格、时间、出版社信息，余下皆为作者信息
        author = ''
        for x in b[:-3]:
            author = author +  ' ' +x
        grade = a.find("span",class_='rating_nums').string
        people_grade = a.find("span",class_='pl').string.split("人评价", 1)[0].replace(" ", "").split()[1]
        try:
            quote  = a.find("span",class_='inq').string
        except:
            quote = None

        print('*'*50+'第{}页第{}本'.format(i+1,j)+'*'*50)
        print('图片链接：{}\n书名：{}\n作者：{}\n出版社：{}\n日期：：{}\n价格：{}\n分数：{}\n评价人数：{}\n名言：{}\n'
              .format(img_href,book_name,author,publisher,date,price,grade,people_grade,quote))

        j += 1




def main():
    for n in range(10):
        url = 'https://book.douban.com/top250?start={}'.format(25 * n)
        # print(url)
        soup = get_soup(url)
        get_htmltext(n,soup)
        time.sleep(1)  # 每爬取一次停止1s在继续爬取

if __name__ == '__main__':
    main()