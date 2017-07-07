# -*- coding: utf-8 -*-
import os
from urllib import parse

import scrapy
from scrapy.http import Request

from MessSpiders.utils.download_image import download_image


class A17jitaSpider(scrapy.Spider):
    name = '17jita'
    allowed_domains = ['www.17jita.com']
    # start_urls = ['http://www.17jita.com/tab/']
    # 图片谱
    start_urls = ['http://www.17jita.com/tab/img/']
    # ukulele谱
    # start_urls = ['http://www.17jita.com/tab/ukulele/']

    def parse(self, response):

        post_nodes = response.css(".bbda .xs2 a::attr(href)").extract()
        for node in post_nodes:
            post_url = node[8:]
            url = parse.urljoin(response.url, post_url)
            try:
                yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_whole_url, dont_filter=False)
            except Exception as e:
                print(e)
        # 下一页的url
        next_url = response.css(".pgs .pg a[class='nxt']::attr(href)").extract_first("")
        if next_url:
            yield Request(url=next_url, callback=self.parse)

    def parse_whole_url(self, response):

        # download_image(response)

        title = response.css(".hm h1::text").extract_first("")
        whole_page_url = response.css(".bm.vw .pg a::attr('href')").extract_first()

        yield Request(url=whole_page_url, callback=self.parse_detail)

    def parse_detail(self, response):
        path = os.getcwd() + "/图片谱"
        if not os.path.exists(path):
            os.makedirs(path)
        title = response.css(".hm h1::text").extract_first("")
        img_urls = response.css("#article_contents a::attr('href')").extract()
        download_image(title, path, img_urls)