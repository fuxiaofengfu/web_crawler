# -*- coding: utf-8 -*-
"""
    create 2017/12/27 15:20
    by xiaofengfu
"""
import hashlib
import sys


def md5(string):
    reload(sys)
    sys.setdefaultencoding("utf-8")
    m = hashlib.md5()
    if not string:
        return None
    m.update(string)
    return m.hexdigest()
