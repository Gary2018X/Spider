import time

import requests
from bs4 import BeautifulSoup
from data_admin import database
# 初始化并连接数据库，主机名默认本地，端口默认3306，用户名默认root，字符集默认utf-8，需要传入数据库密码和数据库名
Data_admin = database(password='Z!20010705!ZB', db='douban')

def get_soup(url = 'https://movie.douban.com/top250?start=0&filter='):
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36'}
    html = requests.get(url,headers=header)  # get方式请求数据
    # print(html.status_code)  # 查看请求的状态码（200表示请求正常）
    html.encoding = html.apparent_encoding  # 设置编码，防止由于编码问题导致文字错乱
    # print(html.text)  # 查看请求到的内容
    content = html.text
    soup = BeautifulSoup(content, "lxml")
    return soup

def get_htmltext(soup):
    div = soup.find_all("div",class_='item')  # 获取所有的div
    for a in div:  # 循环查看每个div的属性
        id = a.find("div",class_='pic').find("em").string  # 获取id
        img_href = a.find("div",class_='pic').find("a").find("img").attrs["src"]  # 获取图片链接
        title = a.find("div",class_='info').find("div",class_='hd').find("a").find_all("span",class_='title')
        Chinese_title = title[0].string  # 获取中文名
        if len(title)== 2:
            English_title = title[1].string  # 获取英文名
        else:
            English_title = None
        # 获取电影其他名称
        other = a.find("div", class_='info').find("div", class_='hd').find("a").find("span", class_='other').string
        #运用.stripped_strings来获取导演、主演等信息
        b = a.find("div", class_='info').find("div", class_='bd').find("p",class_="")
        c =list( b.stripped_strings)
        # print(c[0])
        director = c[0].split("导演: ", 1)[1].split("   主", 1)[0]
        # protagonist = c[0]  # 因简介主演信息不够，故无法收集
        # print(director)
        time = c[1].split(" / ", 1)[0]
        country = c[1].split(" / ", 1)[1].split(" / ", 1)[0]
        type = c[1].split(" / ", 1)[1].split(" / ", 1)[1]
        grade = a.find("div", class_='info').find("div", class_='bd').find("div",class_="star").find("span",class_="rating_num").string
        people_grade = a.find("div", class_='info').find("div", class_='bd').find("div",class_="star").find_all("span")[3].string.split("人", 1)[0]
        try:
            quote = a.find("div", class_='info').find("div", class_='bd').find("p",class_="quote").find("span").string
        except:
            quote = None

        sql = 'insert into top250_info(id,img_href,Chinese_title,English_title,other,director,time,country,type,grade,people_grade,quote) values("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}") ON duplicate KEY UPDATE id=id'.format(id,img_href,Chinese_title,English_title,other,director,time,country,type,grade,people_grade,quote)
        Data_admin.database(sql)
        print(id)

def main():
    for n in range(10):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(25 * n)
        # print(url)
        soup = get_soup(url)
        get_htmltext(soup)
        time.sleep(1)  # 每爬取一次停止1s在继续爬取

if __name__ == '__main__':
    main()




