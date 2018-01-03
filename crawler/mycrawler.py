# -*- coding: utf-8 -*-
"""
    create 2017/12/27 18:42
    by xiaofengfu
"""
import os

import base.config.common_config as common_config
import crawler.util.common_util as util
import crawler.util.file_util as file_util
import crawler.util.uuid_util as myuuid
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
        # 先查找种子库，根据种子库爬取
        sql = """
           select * from seed_url_table where status=0 
           ORDER by update_time desc,crawler_num ASC limit 0,%s FOR UPDATE 
        """
        try:
            result = self.mysql.queryNotClose(sql, [self.url_num])

            if result:  # 有种子,则将种子库给放入到web_url_table中
                for seed in result:
                    self.saveUrlTableByUrl(seed["url"], seed["content_type"], seed["title"], seed["referer"])
                    update_crawler_num = """
                        update seed_url_table set crawler_num = crawler_num + 1,update_time=%s where id=%s
                    """
                    self.mysql.excuteNotCommit(update_crawler_num, [util.now(), seed["id"]])
            # 在web_url_table中选20条放入队列中
            sql = """
                      select * from web_url_table where used=0
                      ORDER BY create_time desc limit 0,%s FOR UPDATE 
                  """
            result = self.mysql.queryNotClose(sql, [self.url_num])
            if result:
                self.parseToActionQueue(result)
            self.mysql.connection.commit()
        except:
            log.getLogger().exception("mycrawler action ...")
        finally:
            self.mysql.close()

    def parseToActionQueue(self, web_url_table_items):
        """
        将web_url表的数据给放入action_queue表中，让多线程消费者去执行爬取任务,
        这里爬取任务(action_queue表的action_str字段)需要单独写脚本,
        example:
        action_str = "/usr/bin/python action_crawler.py crawler_url crawler.title referer"
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
            action_str = self.getActionStr(item["url"], item["title"], item["referer"])
            insert_values.append({
                "action_str": action_str,
                "try_num": common_config.ACTION_TRY_NUM,
                "create_time": now
            })
        if insert_values:
            sql = sql % ",".join(ids)
            self.mysql.excuteNotCommit(sql)
            self.mysql.excuteManyNotCommit(insert_action_queue, insert_values)

    def getActionStr(self, url, title, referer):
        py_path = os.path.dirname(os.path.dirname(__file__))+"/action_crawler.py"
        return "%s %s %s %s %s" % (common_config.PYTHON_PATH, py_path, url, title, referer)

    def saveUrlTableByUrl(self, url, charset="utf-8", title=None, referer=None):
        """
        爬取url并获取到该url页面的所有a标签
        保存到web_url_table表中
        :param url:
        :param charset:
        :param title:
        :param referer:
        :return:
        """
        sql = """
            insert into web_url_table (`url`,`title`,`content_type`,`referer`,
            `hostname`,`params`,`md5`,`url_type`,`used`,`create_time`
            ,`update_time`) VALUES (%(url)s,%(title)s,%(content_type)s,%(referer)s,
            %(hostname)s,%(params)s,%(md5)s,%(url_type)s,%(used)s,
            %(create_time)s,%(update_time)s) ON DUPLICATE KEY UPDATE md5=md5
        """
        params = []
        now = util.now()
        _md5 = md5(url)
        self.html_util = html_util = HtmlURLUtil()
        try:
            params.append({
                "url": url,
                "title": title,
                "content_type": charset,
                "referer": referer,
                "hostname": html_util.getTLD(url),
                "params": html_util.getSortQS(url),
                "md5": _md5,
                "url_type": "0",
                "used": "0",
                "create_time": now,
                "update_time": now
            })
            douban = html_util.getHtml(url)
            # 写入到文件中
            file_path = common_config.CRAWLER_SAVE_PATH+os.sep+"tmp"+os.sep+myuuid.getUUID().__str__()
            self.appendContentToFile(url, title, url, douban, file_path)
            # 查找该页面下的所有的a标签
            eles = html_util.getElementsByTagName("a")
            hsn = html_util.getTLD(url)
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
                            "referer": url,
                            "hostname": html_util.getTLD(sub_url),
                            "params": str(html_util.getSortQS(sub_url)),
                            "md5": sub_md5,
                            "url_type": 0 if hsn == html_util.getTLD(sub_url) else 1,
                            "used": "0",
                            "create_time": now,
                            "update_time": now
                        })
            self.mysql.excuteManyNotCommit(sql, params)
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
        self.html_util.writeWebContentToFile(_str+"\n", file_path)
        des_file = common_config.CRAWLER_SAVE_PATH + os.sep + "done"+os.sep + os.path.basename(file_path)
        file_util.mvFile(file_path, des_file)

    def saveSeedUrl(self, seedurl, title=None):
        """
        保存种子链接,保存到seed_url_table表中
        :param seedurl:
        :param title:
        :return:
        """
        sql = """
                insert into seed_url_table (`url`,`title`,`content_type`,`referer`,
                `hostname`,`params`,`md5`,`status`,`create_time`
                ,`update_time`) VALUES (%(url)s,%(title)s,%(content_type)s,%(referer)s,
                %(hostname)s,%(params)s,%(md5)s,%(status)s,
                %(create_time)s,%(update_time)s) ON DUPLICATE KEY UPDATE md5=md5
             """
        now = util.now()
        _md5 = md5(seedurl)
        self.html_util = html_util = HtmlURLUtil()
        params = {
            "url": seedurl,
            "title": title,
            "content_type": "utf-8",
            "referer": seedurl,
            "hostname": html_util.getTLD(seedurl),
            "params": html_util.getSortQS(seedurl),
            "md5": _md5,
            "status": "0",
            "create_time": now,
            "update_time": now
        }
        self.mysql.excuteCommit(sql, params)
