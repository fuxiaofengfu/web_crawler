# -*- coding: utf-8 -*-
"""
    create 2017/12/27 15:20
    by xiaofengfu
"""
import hashlib


def md5(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()
