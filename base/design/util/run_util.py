# -*- coding: utf-8 -*-
"""
    create 2017/12/25 15:21
    by xiaofengfu
"""
import base.design.consumer.thread_action as consumerThread
import base.design.productor.thread_action as productorThread
import Queue
import time


class Run:

    def __init__(
            self, action, consumer_thread_num=100, consumer_thread_wait_time=60,
            productor_thread_num=100, productor_thread_wait_time=60):

        self.consumer_thread_num = consumer_thread_num
        self.productor_thread_num = productor_thread_num
        self.consumer_thread_wait_time = consumer_thread_wait_time
        self.productor_thread_wait_time = productor_thread_wait_time
        self.action = action

    def work_run(self):
        queue = Queue.Queue()
        for i in range(0, self.productor_thread_num):
            thread_name = "productor_thread_" + str(i)
            productorThread.ProductorThreadAction(
                queue, self.action, self.productor_thread_wait_time, thread_name=thread_name).start()
        time.sleep(5)  # 睡眠5秒

        for i in range(0, self.consumer_thread_num):
            thread_name = "consumer_thread_" + str(i)
            consumerThread.ConsumerQueueAction(
                queue, self.consumer_thread_wait_time, thread_name=thread_name).start()
