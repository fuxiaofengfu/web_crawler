# -*- coding: utf-8 -*-
"""
    create 2017/12/27 18:42
    by xiaofengfu
"""
import os

import base.config.common_config as common_config
import crawler.util.common_util as util
import log.common_log as log
from base.mysql.mysql_util import Mysql
from crawler.util.html_util import HtmlURLUtil
from crawler.util.md5_util import md5


class MyCrawler:

    def __init__(self, url_num=20):
        self.url_num = url_num
        self.mysql = Mysql()
        self.html_util = None

    def action(self):
        """
        crawler主入口,保存需要爬取的url到web_url_table表中,
        并转化到action_queue表中让生产者去取用
        只有在web_url_table里边没有链接的时候才根据提供的top_url取新的链接
        该方法使用定时任务或者线程单独调用
        :return:
        """
        sql = """
          select * from web_url_table where used=0 and md5 <> %s
          ORDER BY create_time desc limit 0,%s FOR UPDATE 
        """
        result = self.mysql.queryNotClose(sql, [md5(common_config.TOP_URL), self.url_num])
        if result:
            self.parseToActionQueue(result)
        else:
            url_items = self.saveSeedWebUrlToMysql(common_config.TOP_URL, "豆瓣")
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
            action_str = self.getActionStr(item["url"], item["title"], item["file_path"])
            insert_values.append({
                "action_str": action_str,
                "try_num": common_config.ACTION_TRY_NUM,
                "create_time": now
            })
        if insert_values:
            sql = sql % ",".join(ids)
            self.mysql.excuteNotCommit(sql)
            self.mysql.excuteManyCommit(insert_action_queue, insert_values)
        else:
            self.mysql.getConnection().close()

    def getActionStr(self, url, title, save_path):
        py_path = os.path.dirname(__file__)+"/action_crawler.py"
        return "%s %s %s %s %s" % (common_config.PYTHON_PATH, py_path, url, title, save_path)

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
        self.html_util = html_util = HtmlURLUtil()
        try:
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
                "file_path": common_config.CRAWLER_SAVE_PATH,
                "create_time": now,
                "update_time": now
            })
            douban = html_util.getHtml(seedurl)
            # html_util.writeWebContentToFile(douban, params[0]["file_path"])
            # 追加到爬取内容的文件中
            self.appendContentToFile(seedurl, title, seedurl, douban, common_config.CRAWLER_SAVE_PATH)
            # 查找该页面下的所有的a标签
            eles = html_util.getElementsByTagName("a")
            hsn = html_util.getTLD(seedurl)
            _charset = html_util.getCharset(douban)
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
                            "content_type": _charset,
                            "referer": seedurl,
                            "hostname": html_util.getTLD(sub_url),
                            "params": str(html_util.getSortQS(sub_url)),
                            "md5": sub_md5,
                            "url_type": 0 if hsn == html_util.getTLD(sub_url) else 1,
                            "used": "0",
                            "file_path": common_config.CRAWLER_SAVE_PATH,
                            "create_time": now,
                            "update_time": now
                        })
            self.mysql.excuteManyCommit(sql, params)
        except:
            log.getLogger().exception("mycrawler saveSeedWebUrlToMysql ...")
        finally:
            html_util.closeWebDriver()
        return params

    def appendContentToFile(self, url, title, referer, content, file_path):
        if not self.html_util:
            self.html_util = HtmlURLUtil()
        content_charset = self.html_util.getCharset(content)
        hostname = self.html_util.getTLD(url)
        create_time = util.now()
        content = util.convertOneLine(content)
        content_md5 = md5(content)
        strlist = []
        strlist.append(url)
        strlist.append(title)
        strlist.append(referer)
        strlist.append(hostname)
        strlist.append(content_charset)
        strlist.append(content_md5)
        strlist.append(create_time)
        strlist.append(content)
        _str = "\001".join(strlist)
        self.html_util.writeWebContentToFile(_str, file_path)


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
