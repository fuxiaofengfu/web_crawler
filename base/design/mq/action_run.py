# -*- coding: utf-8 -*-
"""
    create 2017/12/25 21:34
    by xiaofengfu
"""
import os

import base.config.common_config as common_config
import crawler.util.common_util as util
import log.common_log as log
from base.design.consumer.action import ConsumerAction
from base.design.mq.action_items import ActionItems
from base.design.productor.action import ProductorAction
from base.design.util.run_util import Run
from base.mysql.mysql_util import Mysql


class ConsumerActionImpl(ConsumerAction):

    def __init__(self, action_str, sql_id, params=None, try_num=0, max_try_num=0, fail_num=0):
        super(ConsumerActionImpl, self).__init__(action_str, params, try_num, max_try_num)
        self.sql_id = sql_id
        self.fail_num = fail_num

    def action(self):
        try:
            os.system(self.action_str)
        except:
            log.getLogger().exception("action impl ....action_str:%s" % self.action_str)

    def success(self):
        sql = """
           delete from action_queue where id = %(id)s
        """
        dict_param = {"id": self.sql_id}
        Mysql().excuteCommit(sql, dict_param)

    def fail(self):

        self.fail_num += 1  # 因为保证了同一时间只有一台服务器能拿到该条任务,所以这里可以直接+=1

        if self.max_try_num > self.try_num:
            #  action_status=0,在本线程重试次数未完成前防止其它服务器拿到该action执行
            sql = """
                    update action_queue set finish_time=%(finish_time)s,action_status=0,
                    fail_num=fail_num +1,ip = %(ip)s where id = %(id)s
                  """
        elif self.fail_num >= (self.max_try_num * 3):
            # 如果总的失败次数大于等于失败尝试次数 * 3，则不再尝试执行
            # 即默认被三台服务执行后都失败则认为失败
            sql = """
                    update action_queue set finish_time=%(finish_time)s,action_status=0,
                    ip = %(ip)s where id = %(id)s
            """
        else:
            #  action_status=1尝试了try_num次数后还是失败,则让其它服务器能拿到该ACTION继续执行
            sql = """
                    update action_queue set finish_time=%(finish_time)s,action_status=1,
                    ip = %(ip)s where id = %(id)s
                  """
        ip = util.getIp()
        date = util.now()
        dict_param = {"finish_time": date, "ip": ip, "id": self.sql_id}
        Mysql().excuteCommit(sql, dict_param)


class ProductorActionImpl(ProductorAction):

    def __init__(self):
        super(ProductorActionImpl, self).__init__()

    def action(self):
        items = ActionItems().getActionItems()
        if items:
            consumers = []
            for item in items:
                consumer = ConsumerActionImpl(
                    item["action_str"], item["id"], item["params"],
                    0, item["try_num"]
                )
                consumers.append(consumer)
            return consumers


if __name__ == "__main__":
    """
       执行任务入口
    """
    Run(
        ProductorActionImpl(),
        common_config.CONSUMER_THREAD_NUM,
        common_config.CONSUMER_THREAD_SLEEP,
        common_config.PRODUCTOR_THREAD_NUM,
        common_config.PRODUCTOR_THREAD_SLEEP
    ).work_run()
