# -*- coding: utf-8 -*-
"""
    create 2017/12/29 20:12
    by xiaofengfu
"""
from threading import Thread
import time
import base.design.mq.action_run as action_run
import log.common_log as log
from crawler.mycrawler import MyCrawler


class MyCrawlerThread(Thread):

    def __init__(self):
        super(MyCrawlerThread, self).__init__()

    def run(self):
        while True:
            try:
                MyCrawler().action()
                time.sleep(30)
            except:
                log.getLogger().exception("MyCrawlerThread exception...")


if __name__ == "__main__":
    # 启动消息队列
    action_run.action_run()
    # 启动爬虫
    MyCrawlerThread().start()
