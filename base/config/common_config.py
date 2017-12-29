# -*- coding: utf-8 -*-
"""
    create 2017/12/22 19:01
    by xiaofengfu
"""

# 以下为crawler配置

# 爬取网页内容存放的路径
CRAWLER_SAVE_PATH = "/home/fuxiaofeng/crawler/web_content/crawler.html"
TOP_URL = "https://www.baidu.com/"  # 入口爬取url
PYTHON_PATH = "/usr/local/bin/python"  # python 命令的路径

# 以下为生产者消费者配置
PRODUCTOR_THREAD_NUM = 1  # 生产者线程数
PRODUCTOR_THREAD_SLEEP = 5  # 生产者单个线程随机睡眠时间最大值0-60
CONSUMER_THREAD_NUM = 1  # 消费者线程数
CONSUMER_THREAD_SLEEP = 5  # 消费者单个线程随机睡眠最大时间,0-60
ACTION_TRY_NUM = 3  # 单一action失败重试次数默认值,如果每个action重试不同,需要修改数据库或者在业务里边设置

# 数据库配置
MYSQL_CONFIG = {"user": "mysql",
                "passwd": "12345678",
                "host": "192.168.88.195",
                "port": 5506,
                "db": "hainiureport",
                "charset": "utf8",
                # "ssl": "false",
                "autocommit": False}
