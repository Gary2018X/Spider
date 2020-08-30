# -*- coding: utf-8 -*-
# author:Gary

from selenium import webdriver

# 第一步：创建一个浏览器对象
browser = webdriver.Chrome()
# 第二步：使用浏览器对象对网址发起请求
browser.get("https://www.gary666.com")

# 测试代码
# 获取网页的源代码
print(browser.page_source)
# 获取此次请求的地址
# print(browser.current_url)
# 当前窗口对象
# print(browser.current_window_handle)
# 获取此次请求的cookie信息
# print(browser.get_cookies())
# 退出浏览器的命令，注释掉方便我们查看，正式运行一定要退出
# browser.quit()

# ************************selenium定位html元素************************#
'''
.text方法是获取这个html元素的内容
find_element是只返还一个
需要返回多个可以通过find_elements来获取
'''

'''
1.通过id定位，方法：find_element_by_id()
比如获取我博客的头部导航栏内容，观察html源代码可以发现，其id为topnav，id通常唯一，所以调用find_element_by_id()即可
'''
topnav = browser.find_element_by_id('topnav').text
print('topnav内容', topnav)

'''
1.通过class定位，方法：find_element_by_class_name()
比如获取我博客的logo内容，观察html源代码可以发现，其class为logo，而且只有一个class，所以只要调用然后调用find_element_by_class_name()即可，如果需要获取多个，调用find_elements_by_class_name()
'''
logo = browser.find_element_by_class_name('logo').text
print('logo内容', logo)
browser.quit()
