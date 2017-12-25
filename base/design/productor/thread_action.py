# -*- coding: utf-8 -*-
"""
    create 2017/12/24 12:02
    by xiaofengfu
"""
from threading import Thread
import time, random
import log.common_log as log
import base.exception.consumer_exception as consumerException
import base.design.consumer.action as consumerAction


class ProductorThreadAction(Thread):
    """
      生产者线程
      用于多线程在队列中存入消费者行为
    """
    def __init__(self, queque, action, wait_time=60, max_num=10000, thread_name=None):
        """
        :param queque: 队列对象
        :param wait_time: 每隔多久放一次,最大时间,单位s,随机在0 - wait_time之间
        :param max_num: 一次放入到队列最多action数
        :param thread_name: 线程名称
        :param action: 生产者对象
        """
        super(ProductorThreadAction, self).__init__(name=thread_name)
        self.q = queque
        self.wait_time = wait_time
        self.max_num = max_num
        self.action = action

    def run(self):
        while True:
            que_num = self.q.unfinished_tasks

            if que_num <= self.max_num:  # 只有在队列里边的数量小于等于规定的最大值时,才能继续向队列里边放
                action_items = self.action.action()

            if action_items:
                while action_items:
                    ac = action_items.pop()
                    if not isinstance(ac, consumerAction.ConsumerAction):
                        raise consumerException.ConsumberException("ac is not ConsumerAction's instance...")

                    self.q.put(ac)
            # 放完一波任务休息一波
            s = random.randint(0, self.wait_time)
            log.getProductorLog().info("ProductorThreadAction 休眠时间:%s,队列里边任务数量:%s" % (s, que_num))
            time.sleep(s)
