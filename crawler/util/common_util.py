# -*- coding: utf-8 -*-
"""
    create 2017/12/26 14:37
    by xiaofengfu
"""
import socket
import time
import os


def getIp():
    hostname = socket.gethostname()
    # ip = socket.gethostbyname(hostname)
    addrs = socket.getaddrinfo(hostname, None)
    for item in addrs:
        if ':' not in item[4][0]:
            return item[4][0]


def now():
    # return time.asctime(time.localtime(time.time()))
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def dictListContains(dict_list, dict_key, dict_kvalue):

    if not dict_list:
        return False
    for item in dict_list:
        if dict_key in item:
            if item[dict_key] == dict_kvalue:
                return True
    return False


def getModuleParentPath(module_name):
    return os.path.dirname(module_name.__file__)
