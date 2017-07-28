# -*- coding: utf-8 -*-
import re
import os
import time
import datetime
import json
from urllib import parse

import requests
import scrapy
from scrapy.loader import ItemLoader

# from MessSpiders.items import


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    # question第一页answer的url
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B*%5D.is_normal%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={}limit={}&sort_by=default"

    agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"
    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
        "User-Agent": agent,
    }

    custom_settings = {
        "COOKIES_ENABLED": True,
    }

    # session = requests.session()

    def start_requests(self):
        return [scrapy.Request("https://www.zhihu.com/#signin", headers=self.headers, callback=self.login)]

    def login(self, response):
        response_text = response.text
        # with open("test.html", 'w') as f:
        #     f.write(response_text)

        # re.DOTALL 匹配整个text，否则只会匹配第一行
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text, re.DOTALL)

        if match_obj:
            xsrf = match_obj.group(1)

            post_data = {
                "_xsrf": xsrf,
                "phone_num": os.getenv("phone_num"),
                "password": os.getenv("password"),
                "captcha": "",
            }

            # 生成验证码
            gen_timestamp = str(int(time.time() * 1000))
            captcha_url = "https://www.zhihu.com/captcha.gif?r={}&type=login".format(gen_timestamp)
            yield scrapy.Request(captcha_url, headers=self.headers, meta={"post_data": post_data}, callback=self.login_after_captcha)

    def login_after_captcha(self, response):
        with open("captcha.jpg", "wb") as f:
            f.write(response.body)

        from PIL import Image
        im = Image.open('captcha.jpg')
        im.show()
        im.close()

        captcha = input("输入验证码：\n")

        post_data = response.meta.get("post_data")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data["captcha"] = captcha
        # post_data["captcha_type"] = "cn"

        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login
        )]

    def check_login(self, response):
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"] == "登录成功":
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)

    def parse(self, response):
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        # 过滤不规则url
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            match_obj = re.match("(.*question/(\d+)(/|$)).*", url)
            if match_obj:
                request_url = match_obj.group(1)
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)
            else:
                yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse_question(self, response):
        pass
