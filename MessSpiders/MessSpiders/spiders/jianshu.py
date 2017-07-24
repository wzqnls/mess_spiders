# -*- coding: utf-8 -*-

import pydispatch
from urllib import parse

from selenium import webdriver
import scrapy
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.http import Request


class JianshuSpider(scrapy.Spider):
    name = 'jianshu'
    allowed_domains = ['www.jianshu.com']
    start_urls = ['http://www.jianshu.com/']

    # 有界面运行chrome
    # def __init__(self):
    #     self.browser = webdriver.Chrome(executable_path="/home/lee/Downloads/chromedriver")
    #     super(JianshuSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)

    # 无界面运行chrome
    def __init__(self):
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(800, 600))
        display.start()

        self.browser = webdriver.Chrome(executable_path="/home/lee/Downloads/chromedriver")
        super(JianshuSpider, self).__init__()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(JianshuSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        # 当爬虫退出的时候，关闭chrome
        print("spider closed")
        self.browser.quit()

    def parse(self, response):

        # note_lists = response.css(".note-list a[class='title']::attr(href)").extract()
        # for note_url in note_lists:
        #     yield Request(url=parse.urljoin(response.url, note_url), callback=self.parse_detail)
        #
        # more_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        # if more_url:
        #     yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
        pass
