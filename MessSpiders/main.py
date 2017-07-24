#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-7-7 上午11:12
# @Author  : Lee
# @File    : main.py

import sys
import os

from scrapy.cmdline import execute


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "17jita"])
# execute(["scrapy", "crawl", "jobbole"])
execute(["scrapy", "crawl", "jianshu"])