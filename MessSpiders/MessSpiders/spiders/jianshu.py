# -*- coding: utf-8 -*-

from urllib import parse

import scrapy
from scrapy.http import Request


class JianshuSpider(scrapy.Spider):
    name = 'jianshu'
    allowed_domains = ['www.jianshu.com']
    start_urls = ['http://www.jianshu.com/']

    def parse(self, response):

        note_lists = response.css(".note-list a[class='title']::attr(href)").extract()
        for note_url in note_lists:
            yield Request(url=parse.urljoin(response.url, note_url), callback=self.parse_detail)

        more_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if more_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
