#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/18 22:46
# @Author  : Lee
# @File    : common.py
# @Software: PyCharm

import hashlib


def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()