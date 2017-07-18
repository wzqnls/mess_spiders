#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-7-7 下午1:48
# @Author  : Lee
# @File    : dwonload_image.py

import os
import requests


def download_image(direct_name, cur_path=os.getcwd(), *kwgs):
    img_path = cur_path + os.sep + "".join(direct_name.split(' '))
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    num = 1
    for url in kwgs[0]:
        suffix = os.path.splitext(url)[1]
        name = direct_name.split(' ')[0].strip()
        filename = "{name}{num}{suffix}".format(name=name, num=num, suffix=suffix)
        filepath = os.path.join(img_path, filename)

        with open(filepath, 'wb') as f:
            f.write(requests.get(url).content)
        num += 1
