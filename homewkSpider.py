# -*- coding: utf-8 -*-
# author:Gary
import requests

from bs4 import BeautifulSoup  # 解析网页内容

import hashlib
# MD5加密
def md5value(password):
    password = password.encode()
    md5 = hashlib.md5()
    md5.update(password)
    return md5.hexdigest()


def post_data(username, password):
    url = 'https://homewk.cn/login'  # 登录的url
    data = {
        'username': username,
        'password': md5value(str(password)),
        'identity_id': 'Student'
    }  # 需要post的数据
    res = requests.post(url, data)
    if res.status_code == 200:  # 状态码200表示请求成功
        return res.text  # 返回网页的内容
    else:
        print('ISE')
        exit()


def login(html):
    # print(html)
    soup = BeautifulSoup(html, 'html.parser')  # 注意需要添加html.parser解析
    error_div = soup.find('div', id='msg')  # 定位到div
    if error_div:  # 如果这个标签存在就表示登录失败
        print(error_div.find_next('h1').text)  # 输入错误提示
    else:
        print('login successfully!')

    # 或者判断登录成功的特有标签，可以登录成功的欢迎语
    # name_span = soup.find_all('span', class_='l-btn-text')  # 如果你观察过通过html的检查观察，会发现欢迎语是在这个span
    # 但是你获取不到内容，因为这个是经过js控制变化了，我们代码没有执行js，所以获取到的网页内容就不一样
    # 这个时候你就要输出网页内容观察，然后你就会发现，他其实在下面的div中，而且唯一
    name_div = soup.find('div', class_='easyui-menubutton')
    if name_div:  # 存在表示登录成功
        print(name_div.text)
    else:
        print('login failure!')


if __name__ == '__main__':

    # print(res.text)
    # 判断是否登录成功，判断特点的不同元素是否出现，比如我们获取你的姓名是否出现在返回的页面内容中
    # 获取到了证明登录成功了，没获取到证明失败了，
    # 也可以通过判断特定的html标签是否出现
    username = 2018301040111  # 学号不存在会报错ise
    password = '123456'  # 密码得是字符串
    html = post_data(username, password)
    # 方法一，特定内容是否出现，比如登录成功后会有姓名
    if '熊廷顺' in html:
        print('login successfully!')
    else:
        print('login failure!')

    # 方法二，特定html标签是否出现
    login(html)
