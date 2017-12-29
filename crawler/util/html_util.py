# -*- coding: utf-8 -*-
"""
    create 2017/12/27 14:20
    by xiaofengfu
"""
import re
import sys
import urllib
import urlparse

import tld
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.phantomjs.webdriver import WebDriver

import crawler.util.md5_util as md5_util
import crawler.util.sort_util as sort_util
import log.common_log as log


class HtmlURLUtil:
    """
        html请求工具类
        urllib:python核心库,一般只用于对url的处理,不用它提供的request请求
        tld(top level domain):强大的url域名处理工具,好吧,也不是很强大,但是用着方便
        selenium强大的,NB的web自动化测试工具
        phantomJS:无界面的webkit,一般使用它的request,好处,可以爬取搜索引擎的结果(benefit ajax)
    """
    __USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) " \
                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"

    def __init__(self, driver=None):
        self.driver = driver
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            # 'Accept-Encoding': '*',
            'Cache-Control': 'max-age=0',
            'User-Agent': HtmlURLUtil.__USER_AGENT,
            'Connection': 'keep-alive',
            'Referer': 'https://www.baidu.com/'
        }

    def getHtml(self, url, referer="https://www.baidu.com/"):
        try:
            my_dc = DesiredCapabilities.PHANTOMJS.copy()
            my_dc["browserName"] = "chrome"
            my_dc["platform"] = "mac"
            my_dc["version"] = "63.0.3239.84"
            my_dc["phantomjs.page.settings.loadImages"] = False
            my_dc["phantomjs.page.settings.userAgent"] = HtmlURLUtil.__USER_AGENT

            service_args = ["--load-images=false", "--disk-cache=false",
                            "--ignore-ssl-errors=true"]
            # "--webdriver-logfile=webdriver.log","--webdriver-loglevel=INFO"
            for head, value in self.headers.iteritems():
                my_dc["phantomjs.page.customHeaders.{}".format(head)] = value

            my_dc["phantomjs.page.customHeaders.Referer"] = referer
            self.driver = WebDriver(desired_capabilities=my_dc, service_args=service_args)
            self.driver.set_script_timeout(20)
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(5)
            self.driver.set_window_size(2560, 1066)

            self.driver.get(url)
            # 保存网页快照图片
            # self.driver.save_screenshot(md5_util.md5(url)+".png")
            _result = self.driver.page_source
        except:
            log.getLogger().exception("HtmlURLUtil  getHtml error...")
            # self.driver.close()
            self.driver.quit()

        return _result

    def closeWebDriver(self):
        self.driver.quit()

    def getSortQS(self, url):
        """
        获取排序好的query string
        :param url:
        :return:
        """
        a = urllib.splitquery(url)
        if len(a) <= 1 or not a[1]:
            return None
        qs = urlparse.parse_qs(a[1])
        # 使用快速排序O(nlogn)
        return sort_util.fastSortDict(qs)

    def getTLD(self, url):
        """
        获取域名对象
        :param url:
        :return:
        """
        try:
            web = urllib.splitquery(url)[0]
            return tld.get_tld(web)
        except:
            log.getLogger().exception("getTLD ...%s" % url)
        return None

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

    def getElementsByTagName(self, elname):
        return self.driver.find_elements_by_tag_name(elname)

    def writeWebContentToFile(self, webcontent, filepath):
        if not webcontent:
            return
        reload(sys)
        sys.setdefaultencoding("utf-8")
        try:
            f = open(filepath, "a")
            f.write(webcontent)
            f.flush()
        except:
            log.getLogger().exception("htmlutil writeWebContentToFile ...")
        finally:
            f.close()

    def getCharset(self, content):

        charset = "utf-8"
        m = re.compile('<meta .*(http-equiv="?Content-Type"?.*)?charset="?([a-zA-Z0-9_-]+)"?', re.I)\
            .search(content)
        if m and m.lastindex == 2:
            charset = m.group(2).lower()
        return charset

