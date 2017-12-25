# -*- coding: utf-8 -*-
"""
    create 2017/12/24 12:03
    by xiaofengfu
"""
from threading import Thread
import time, random
import base.exception.consumer_exception as consumerException
import log.common_log as log
import base.design.consumer.action as consumerAction

class ConsumerQueueAction(Thread):

    def __init__(self, queue, wait_time=60, max_num=200, thread_name=None):
        super(ConsumerQueueAction, self).__init__(name=thread_name)
        self.q = queue
        self.wait_time = wait_time
        self.max_num = max_num

    def run(self):

        while True:
            que_num = self.q.unfinished_tasks
            if que_num:
                begin_time = time.clock()
                action = self.q.get()

                if not isinstance(action, consumerAction.ConsumerAction):
                    raise consumerException.ConsumberException("action is not ConsumerAction's instance...")

                action_result = action.run()  # 执行action任务

                # 如果action重试次数小于最大重试的次数,则重试
                if not action_result and action.max_try_num > action.try_num:
                    self.q.put(action)
                    action.try_num += 1
                    log.getConsumerLog().error("重试 %s,max_try_num=%s,try_num=%s" \
                                               % (action.action_str, action.max_try_num, action.try_num))
                self.q.task_done()
                end_time = time.clock()
                log.getConsumerLog().info("consumer action执行时间%s" % (end_time - begin_time))
            # 睡眠一波
            s = random.randint(0, self.wait_time)
            log.getConsumerLog().info("ConsumerQueueAction休眠时间:%s,队列里边数量:%s" % (s,que_num))
            time.sleep(s)
