# -*- coding: utf-8 -*-
"""
    create 2017/12/28 20:24
    by xiaofengfu
"""
import sys

import base.config.common_config as common_log
import log.common_log as log
from base.exception.consumer_exception import ConsumberException
from crawler.mycrawler import MyCrawler
from crawler.util.html_util import HtmlURLUtil

if __name__ == "__main__":
    """
      爬取链接动作,供消费者(ConsumerAction)调用
      sys.argv = ['/Users/xiaofengfu/Documents/pythonscript/fxf_crawler/crawler/action_crawler.py', 
      'http://xclient.info/', 
      'ma精品应用', 
      'referer']
    """
    reload(sys)
    sys.setdefaultencoding("utf-8")

    log.getLogger().info(sys.argv)

    if not sys.argv or len(sys.argv) <= 3:
        raise ConsumberException("请设置需要爬取的url,title,referer")

    html_util = HtmlURLUtil()
    # url, title, referer, save_path
    url = sys.argv[1]
    title = sys.argv[2]
    referer = sys.argv[3]

    html_result = html_util.getHtml(url)
    my_crawler = MyCrawler()
    my_crawler.appendContentToFile(url, title, referer, html_result, common_log.CRAWLER_SAVE_PATH)
    my_crawler.saveSeedWebUrlToMysql(url, title)
