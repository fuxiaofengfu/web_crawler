# -*- coding: utf-8 -*-
"""
    create 2017/12/26 14:37
    by xiaofengfu
"""
import socket
import time


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
