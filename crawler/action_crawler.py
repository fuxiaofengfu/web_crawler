# -*- coding: utf-8 -*-
"""
    create 2017/12/28 20:24
    by xiaofengfu
"""
import sys

from base.exception.consumer_exception import ConsumberException
from crawler.mycrawler import MyCrawler
from crawler.util.html_util import HtmlURLUtil

if __name__ == "__main__":
    """
      爬取链接动作,供消费者(ConsumerAction)调用
    """
    if not sys.argv:
        raise ConsumberException("请设置需要爬取的url,title,file_path")

    html_util = HtmlURLUtil()
    html_result = html_util.getHtml(sys.argv[0])
    html_util.writeWebContentToFile(html_result, sys.argv[2])
    my_crawler = MyCrawler()
    my_crawler.saveSeedWebUrlToMysql(sys.argv[0], sys.argv[1])
