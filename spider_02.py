import time

import requests
from bs4 import BeautifulSoup


def get_soup(url = 'https://gary666.com/learn'):
    html = requests.get(url)  # get方式请求数据
    # print(html.status_code)  # 查看请求的状态码（200表示请求正常）
    html.encoding = html.apparent_encoding  # 设置编码，防止由于编码问题导致文字错乱
    # print(html.text)  # 查看请求到的内容
    content = html.text
    soup = BeautifulSoup(content, "lxml")
    return soup

def get_url(soup):
    a_list = soup.find_all("a", class_='four')  # 获取所有的超链接
    url = []
    for a in a_list:  # 循环查看每个超链接的文字和url
        if a.string is None:  # 如果超链接的内容为空
            continue
        else:
            url.append("https://gary666.com" + a.get("href"))
    return url

def get_htmltext(i,soup):
    div = soup.find_all("div", class_='blogs')  # 获取所有的div
    j = 1
    for a in div:  # 循环查看每个div的属性
        print("=" * 50 + "{}".format(j) + "=" * 50)
        print("第{}页第{}篇".format(i,j))
        j += 1
        title = a.find("h3").find("a").string  # 获取标题
        print("标题：" + title)
        img = a.find("span").find("a").find("img").attrs["src"]  # 获取图片链接
        print("图片链接：" + "https://gary666.com" + img.split("..", 1)[1])
        p = a.find("p").string
        print("内容：" + p)
        author = a.find("li", class_="author").find("a").string
        print("作者：" + author)
        lmname = a.find("li", class_="lmname").find("a").string
        print("文章分类：" + lmname)
        timer = a.find("li", class_="timer").string
        print("时间：" + timer)

def main():
    soup = get_soup()
    url = get_url(soup)
    i = 1
    for n in url:
        soup = get_soup(n)
        get_htmltext(i,soup)
        i += 1
        time.sleep(1)  # 每爬取一次停止1s在继续爬取


if __name__ == '__main__':
    main()



