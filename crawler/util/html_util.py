# -*- coding: utf-8 -*-
"""
    create 2017/12/27 14:20
    by xiaofengfu
"""
import urllib
import urlparse

import tld
from selenium.webdriver.phantomjs.webdriver import WebDriver

import crawler.util.md5_util as md5_util
import crawler.util.sort_util as sort_util


class HtmlURLUtil:
    """
        html请求工具类
        urllib:python核心库,一般只用于对url的处理,不用它提供的request请求
        tld(top level domain):强大的url域名处理工具,好吧,也不是很强大,但是用着方便
        selenium强大的,NB的web自动化测试工具
        phantomJS:无界面的webkit,一般使用它的request,好处,可以爬取搜索引擎的结果(benefit ajax)
    """
    def __init__(self, driver=None):
        self.driver = driver

    def getHtml(self, url):
        self.driver = WebDriver()
        self.driver.get(url)
        _result = self.driver.page_source
        self.driver.close()
        return _result

    def getSortQS(self, url):
        """
        获取排序好的query string
        :param url:
        :return:
        """
        qs = urlparse.parse_qs(urllib.splitquery(url)[1])
        # 使用快速排序O(nlogn)
        return sort_util.fastSortDict(qs)

    def getTLD(self, url):
        """
        获取域名对象
        :param url:
        :return:
        """
        web = urllib.splitquery(url)[0]
        return tld.get_tld(web, as_object=True)

    def getMd5URL(self, url):
        """
        对url进行md5
        先对参数排序,然后进行md5
        :param url:
        :return:
        """
        web = urllib.splitquery(url)[0]
        string = web + str(self.getSortQS(url))
        return md5_util.md5(string)
