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
      sys.argv = ['/Users/xiaofengfu/Documents/pythonscript/fxf_crawler/crawler/action_crawler.py', 
      'http://xclient.info/', 
      'ma精品应用', 
      '/Users/xiaofengfu/Documents/pythonscript/fxf_crawler/crawler_content/2e7f5eeeb04.html']
    """
    reload(sys)
    sys.setdefaultencoding("utf-8")
    if not sys.argv or len(sys.argv) <= 3:
        raise ConsumberException("请设置需要爬取的url,title,file_path")

    html_util = HtmlURLUtil()
    html_result = html_util.getHtml(sys.argv[1])
    html_util.writeWebContentToFile(html_result, sys.argv[3])
    my_crawler = MyCrawler()
    my_crawler.saveSeedWebUrlToMysql(sys.argv[1], sys.argv[2])
