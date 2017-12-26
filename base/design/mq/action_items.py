# -*- coding: utf-8 -*-
"""
    create 2017/12/25 21:34
    by xiaofengfu
"""
from MySQLdb.cursors import *

import base.design.util.common_util as util
from base.mysql.mysql_util import Mysql


class ActionItems:

    def __init__(self, action_num=20):
        self.action_num = action_num

    def getActionItems(self):
        """
        每次取最新的action_num条数
        并修改状态为执行成功
        :return:
        """
        sql = """
           select * from action_queue WHERE action_status=1 and (ip is NULL or ip <> %s)
           ORDER BY create_time DESC limit 0,%s FOR UPDATE
        """
        db = Mysql()
        params = [util.getIp(), self.action_num]
        result = db.queryNotClose(sql, params, DictCursor)
        if result:
            sql = """
                update action_queue set action_status=2
                WHERE id IN (%s)
            """
            ids = []
            for item in result:
                _id = item["id"]
                ids.append(str(_id))
            sql = sql % ",".join(ids)
            db.excuteCommit(sql)
        return result
