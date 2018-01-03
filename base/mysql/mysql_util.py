# -*- coding: utf-8 -*-
"""
    create 2017/12/25 18:57
    by xiaofengfu
"""
import MySQLdb
from MySQLdb.cursors import *

import base.config.common_config as common_config
import log.common_log as log


class Mysql:
    """
      mysql 链接工具类,提供curd
    """
    def __init__(self):
        self.connection = MySQLdb.connect(
            user=common_config.MYSQL_CONFIG.get("user"),
            passwd=common_config.MYSQL_CONFIG.get("passwd"),
            host=common_config.MYSQL_CONFIG.get("host"),
            port=common_config.MYSQL_CONFIG.get("port"),
            db=common_config.MYSQL_CONFIG.get("db"),
            charset=common_config.MYSQL_CONFIG.get("charset"),
            autocommit=common_config.MYSQL_CONFIG["autocommit"]
        )

    def queryClose(self, query, params=None, cursor_class=DictCursor):
        """
        带参数查询
        :param query:
        :param params:  推荐使用dict类型的,这样可读性最高
        :param cursor_class:  游标类,这里默认为字典游标
        :return:
        """
        try:
            cursor = self.connection.cursor(cursorclass=cursor_class)
            cursor.execute(query, params)
            result = cursor.fetchall()
        except:
            log.getLogger().exception("query dict exception .....")
        finally:
            self.connection.close()
        return result

    def queryNotClose(self, query, params=None, cursor_class=DictCursor):
        """
        带参数查询
        :param query:
        :param params:  推荐使用dict类型的,这样可读性最高
        :param cursor_class:  游标类,这里默认为字典游标
        :return:
        """
        try:
            cursor = self.connection.cursor(cursorclass=cursor_class)
            cursor.execute(query, params)
            result = cursor.fetchall()
        except:
            log.getLogger().exception("query dict exception .....")
        return result

    def excuteCommit(self, query, params=None):
        """
        :param query:
        :param params: 参数建议同  queryDict
        :return:
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
        except:
            self.connection.rollback()
            log.getLogger().exception("excute commit exception .....")
        finally:
            cursor.close()
            self.connection.close()

    def excuteNotCommit(self, query, params=None):
        """
        :param query:
        :param params: 参数建议同  queryDict
        :return:
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
        except:
            log.getLogger().exception("excute not commit exception .....")
            self.connection.rollback()

    def excuteManyNotCommit(self, query, params):
        """
        :param query:
        :param params: 参数建议同  queryDict
        :return:
        """
        try:
            cursor = self.connection.cursor()
            cursor.executemany(query, params)
        except:
            self.connection.rollback()
            log.getLogger().exception("excute commit exception .....")

    def excuteManyCommit(self, query, params):
        """
        :param query:
        :param params: 参数建议同  queryDict
        :return:
        """
        try:
            self.connection.begin()
            cursor = self.connection.cursor()
            cursor.executemany(query, params)
            self.commit()
        except:
            self.connection.rollback()
            log.getLogger().exception("excute commit exception .....")

    def close(self):
        """
        提交事务动作
        :return:
        """
        try:
            self.connection.close()
        except:
            log.getLogger().exception("close exception .....")
