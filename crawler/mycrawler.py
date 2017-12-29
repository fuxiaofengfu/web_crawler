# -*- coding: utf-8 -*-
"""
    create 2017/12/27 18:42
    by xiaofengfu
"""
import os

import crawler.util.common_util as util
from base.mysql.mysql_util import Mysql
from crawler.util.html_util import HtmlURLUtil
from crawler.util.md5_util import md5


class MyCrawler:

    __WEB_CONTENT_PATH = "/Users/xiaofengfu/Documents/pythonscript/fxf_crawler/crawler_content"
    __TOP_URL = "https://www.douban.com/"

    def __init__(self, url_num=20, mysql=None):
        self.url_num = url_num
        self.mysql = Mysql()

    def action(self):
        sql = """
          select * from web_url_table where used=0 and md5 <> %s
          ORDER BY create_time desc limit 0,%s FOR UPDATE 
        """
        result = self.mysql.queryNotClose(sql, [md5(MyCrawler.__TOP_URL), self.url_num])
        if result:
            self.parseToActionQueue(result)
        else:
            url_items = self.saveSeedWebUrlToMysql(MyCrawler.__TOP_URL, "豆瓣")
            return url_items

    def parseToActionQueue(self, web_url_table_items):
        """
        将web_url表的数据给放入action_queue表中，让多线程消费者去执行爬取任务,
        这里爬取任务(action_queue表的action_str字段)需要单独写脚本,
        example:
        action_str = "/usr/bin/python action_crawler.py crawler_url crawler.title crawler_save_path"
        在消费者线程中使用os.system(action_str)
        详见下面test方法
        :param web_url_table_items:
        :return:
        """
        if not web_url_table_items:
            return
        sql = """
            update web_url_table set used=1 where id in (%s)
        """
        ids = []
        now = util.now()
        insert_action_queue = """
           insert into action_queue (action_str,try_num,create_time) 
           VALUES (%(action_str)s,%(try_num)s,%(create_time)s)
        """
        insert_values = []
        for item in web_url_table_items:
            ids.append(str(item["id"]))
            action_str = "/usr/bin/python action_crawler.py "+item["url"]+" "+item["title"]+" "+item["file_path"]
            insert_values.append({
                "action_str": action_str,
                "try_num": 3,
                "create_time": now
            })
        if insert_values:
            sql = sql % ",".join(ids)
            self.mysql.excuteNotCommit(sql)
            self.mysql.excuteManyCommit(insert_action_queue, insert_values)
        else:
            self.mysql.getConnection().close()

    def saveSeedWebUrlToMysql(self, seedurl, title="种子链接"):
        """
        将要爬取的种子链接页面里边的链接放入表中，没有分表分库，简单处理
        :param seedurl: 种子链接
        :param title:  标题
        :return:
        """
        sql = """
            insert into web_url_table (`url`,`title`,`content_type`,`referer`,
            `hostname`,`params`,`md5`,`url_type`,`used`,`file_path`,`create_time`
            ,`update_time`) VALUES (%(url)s,%(title)s,%(content_type)s,%(referer)s,
            %(hostname)s,%(params)s,%(md5)s,%(url_type)s,%(used)s,%(file_path)s,
            %(create_time)s,%(update_time)s) ON DUPLICATE KEY UPDATE md5=md5
        """
        params = []
        now = util.now()
        _md5 = md5(seedurl)
        html_util = HtmlURLUtil()
        params.append({
            "url": seedurl,
            "title": title,
            "content_type": "utf-8",
            "referer": seedurl,
            "hostname": html_util.getTLD(seedurl),
            "params": html_util.getSortQS(seedurl),
            "md5": _md5,
            "url_type": "0",
            "used": "0",
            "file_path": MyCrawler.__WEB_CONTENT_PATH+os.sep+html_util.getMd5URL(seedurl)+".html",
            "create_time": now,
            "update_time": now
        })
        douban = html_util.getHtml(seedurl)
        html_util.writeWebContentToFile(douban, params[0]["file_path"])
        eles = html_util.getElementsByTagName("a")
        hsn = html_util.getTLD(seedurl)
        if eles:
            for el in eles:
                sub_url = el.get_attribute('href')
                if sub_url.count("javascript"):
                    continue
                sub_md5 = md5(sub_url)
                if not util.dictListContains(params, "md5", sub_md5):
                    params.append({
                        "url": sub_url,
                        "title": html_util.driver.title,
                        "content_type": html_util.getCharset(),
                        "referer": seedurl,
                        "hostname": html_util.getTLD(sub_url),
                        "params": str(html_util.getSortQS(sub_url)),
                        "md5": sub_md5,
                        "url_type": 0 if hsn == html_util.getTLD(sub_url) else 1,
                        "used": "0",
                        "file_path": MyCrawler.__WEB_CONTENT_PATH + os.sep + html_util.getMd5URL(sub_url)+".png",
                        "create_time": now,
                        "update_time": now
                    })
        print params
        self.mysql.excuteManyCommit(sql, params)
        return params


if __name__ == "__main__":
    my_crawler = MyCrawler()
    my_crawler.action()


def test():
    command = "/usr/bin/python "
    py_path = "/Users/xiaofengfu/Documents/pythonscript/fxf_crawler/crawler/action_crawler.py "
    url = "http://xclient.info/ "
    title = "mac应用 "
    save_path = "/Users/xiaofengfu/Documents/pythonscript/fxf_crawler/crawler_content/2e7f5eeeb04.html"

    action_str = command + py_path + url + title + save_path
    os.system(action_str)
