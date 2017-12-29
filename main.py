# -*- coding: utf-8 -*-
"""
    create 2017/12/29 20:12
    by xiaofengfu
"""
import base.design.mq.action_run as action_run
import log
import test
from crawler.mycrawler import MyCrawler

if __name__ == "__main__":
    action_run.action_run()
    MyCrawler().action()
