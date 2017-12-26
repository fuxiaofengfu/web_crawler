# -*- coding: utf-8 -*-
"""
    create 2017/12/24 12:54
    by xiaofengfu
"""

from base.mysql.mysql_util import Mysql
import base.design.util.common_util as util

sql = """
   update action_queue set create_time=%s
"""

Mysql().excuteCommit(sql, [util.now()])
