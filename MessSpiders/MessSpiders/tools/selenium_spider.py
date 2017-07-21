#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-7-20 下午3:44
# @Author  : Lee
# @File    : selenium_spider.py
import time
from selenium import webdriver

# browser = webdriver.Chrome(executable_path="/home/lee/Downloads/chromedriver")
#
# browser.get("http://www.jianshu.com/")

# print(browser.page_source)
# for i in range(2):
#     browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
#     time.sleep(3)
#
# print(browser.page_source)

# 设置chromedriver不加载图片
chrome_opt = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_opt.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(executable_path="/home/lee/Downloads/chromedriver", chrome_options=chrome_opt)

browser.get("http://www.jianshu.com/")


# browser.quit()