# -*- coding: utf-8 -*-
"""
    create 2017/12/28 20:24
    by xiaofengfu
"""
import sys

import log.common_log as log
import base.config.common_config as common_log
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

    log.getLogger().info(sys.argv)

    if not sys.argv or len(sys.argv) <= 3:
        raise ConsumberException("请设置需要爬取的url,title,file_path")

    html_util = HtmlURLUtil()
    html_result = html_util.getHtml(sys.argv[1])
    my_crawler = MyCrawler()
    # html_util.writeWebContentToFile(html_result, sys.argv[3])
    my_crawler.appendContentToFile(
        sys.argv[1], sys.argv[2], sys.argv[1], html_result, common_log.CRAWLER_SAVE_PATH)
    my_crawler.saveSeedWebUrlToMysql(sys.argv[1], sys.argv[2])
