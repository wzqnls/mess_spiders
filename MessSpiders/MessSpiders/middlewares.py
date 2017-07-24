# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy import Selector
from scrapy.http import HtmlResponse
from selenium import webdriver
from pyvirtualdisplay import Display

class MessspidersSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JsPageMiddleware(object):

    # def __init__(self):
    #     self.browser = webdriver.Chrome(executable_path="/home/lee/Downloads/chromedriver")
    #     super(JsPageMiddleware, self).__init__()

    # 通过chrome请求动态网页
    @staticmethod
    def process_request(request, spider):
        if spider.name == "jianshu":

            spider.browser.get(request.url)
            import time
            time.sleep(3)
            print("访问{}".format(request.url))

            load_more = spider.browser.find_element_by_css_selector(".load-more a::attr('href')").extract_first("")
            if not load_more:
                pass

            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding='utf8', request=request)
