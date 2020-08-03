import time

import requests
from bs4 import BeautifulSoup
from lxml import etree

# 传入url参数，返回爬取到的网页
def get_soup(url = 'https://book.douban.com/top250?start=0'):
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36'}
    res = requests.get(url=url,headers=header)  # get方式请求数据
    # print(res.status_code)  # 查看请求的状态码（200表示请求正常）
    res.encoding = res.apparent_encoding  # 设置编码，防止由于编码问题导致文字错乱
    # print(html.text)  # 查看请求到的内容
    # res.text就是获取把网页内容转为字符串
    content = res.text
    # print(content)
    # 利用 etree.HTML 把字符串解析成 HTML 文件
    html = etree.HTML(content)
    # print(soup)
    return html

#传入网页内容，对其进行进一步的划分获取到想要的内容
def get_htmltext(i,html):
    # 通过搜索table来展示本页所拥有的书籍数量
    table = html.xpath('//*[@id="content"]/div/div[1]/div/table')
    # print(len(table))  # 展示本页书籍数量
    for j in range(len(table)):
        img_href = html.xpath('//td[1]/a/img/@src')[j]
        book_name = html.xpath('//td[2]/div[1]/a//@title')[j]
        #获取包括作者、出版社、出版日期、价格等的信息
        total = html.xpath('//td[2]/p[1]/text()')[j].split(" / ")
        price = total[-1]
        date = total[-2]
        publisher = total[-3]
        #从尾部开始剥离价格、时间、出版社信息，余下皆为作者信息
        author = ''
        for x in total[:-3]:
            author = author + ' ' + x
        grade = html.xpath('//td[2]/div[2]/span[2]/text()')[j]
        people_grade = html.xpath('//td[2]/div[2]/span[3]/text()')[j].split("人评价", 1)[0].replace(" ", "").split()[1]
        try:
            quote = html.xpath('//td[2]/p[2]/span/text()')[j]
        except:
            quote = None
        print('*' * 50 + '第{}页第{}本'.format(i+1, j+1) + '*' * 50)
        print('图片链接：{}\n书名：{}\n作者：{}\n出版社：{}\n日期：：{}\n价格：{}\n分数：{}\n评价人数：{}\n名言：{}\n'
              .format(img_href, book_name, author, publisher, date, price, grade, people_grade, quote))


def main():
    for n in range(10):
        url = 'https://book.douban.com/top250?start={}'.format(25 * n)
        # print(url)
        soup = get_soup(url)
        get_htmltext(n,soup)
        time.sleep(1)  # 每爬取一次停止1s在继续爬取

if __name__ == '__main__':
    main()