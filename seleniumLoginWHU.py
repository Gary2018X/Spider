#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author : Gary

import time
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-automation'])#提示浏览器不是selenium
chrome_options.add_argument('--headless')  # 无头
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')  # 这个配置很重要
chrome_options.add_experimental_option('excludeSwitches',
                                       ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium


class Selenium:
    def __init__(self):
        # self.driver = webdriver.Chrome(options=chrome_options)  # 有配置的初始化浏览器
        self.driver = webdriver.Chrome()  # 不使用有配置的，方便看操作
        self.driver.maximize_window()  # 窗口最大化

    def login(self, username, password):
        self.driver.get('http://ehall.whu.edu.cn/appShow?appId=5382714380693158')  # 走信息门户认证的教务系统url，不用输入验证码
        # 找到输入框并输入账号密码
        Username = self.driver.find_element_by_id("username")
        Username.send_keys(username)
        Password = self.driver.find_element_by_id("password")
        Password.send_keys(password)
        time.sleep(0.2)
        self.driver.find_element_by_xpath('//*[@id="casLoginForm"]/p[5]/button').click()  # 登录按钮
        try:
            # name=self.driver.find_element_by_id("ampHeaderToolUserName").text#获取姓名,内容为空，弃用
            name = self.driver.find_element_by_id("nameLable").text  # 获取学生姓名
            acade = self.driver.find_element_by_id("acade").text  # 获取学生院系
            # cookies = self.driver.get_cookies()[0]
            # print('登录成功 ...')
            # self.driver.quit()
            # html = self.driver.execute_script("return document.documentElement.outerHTML")
            html = self.driver.find_element_by_xpath('//*[@id="system"]').get_attribute('onclick')
            # 不要用 driver.page_source，那样得到的页面源码不标准
            # print(html)
            csrftoken = html.split(",")[0].split('csrftoken=')[-1]
            print('登录成功！')
            return True, acade, name, self.driver.get_cookies(), csrftoken

        except Exception as e:
            print(str(e))
            try:
                msg = self.driver.find_element_by_id("msg").text
            except Exception as e:
                # time.sleep(5)
                # cpatchaError=self.driver.find_element_by_id("cpatchaError").text
                print(str(e))
                msg = '您尝试的次数过多，请明天再试！或解决方案:通过浏览器成功登录一次信息门户。再重试认证本系统'
            # self.driver.quit()
            return False, msg


if __name__ == '__main__':
    username = 'test'  # 你的信息门户账号
    password = 'test'  # 你的信息门户账号对应的密码
    spider = Selenium()
    print(spider.login(username=username, password=password))  # 查看登录结果
