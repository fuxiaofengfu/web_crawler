# -*- coding: utf-8 -*-
"""
    create 2017/12/24 12:02
    by xiaofengfu
"""
import log.common_log as log
from abc import abstractmethod
from abc import ABCMeta


class ConsumerAction(object):
    """
    python中没有像java的抽象方法一说,所以这里定义的方法只是告诉继承该类的子类
    需要实现哪些方法,类似定义了一个约束
    这里为了实现类似java抽象方法,使用了abc库
    """

    __metaclass__ = ABCMeta

    def __init__(self, action_str, params=None, try_num=0, max_try_num=0):
        self.action_str = action_str
        self.params = params
        self.try_num = try_num
        self.max_try_num = max_try_num

    def run(self):
        try:
            self.action()
            self.success()
            return True
        except:
            self.fail()
            log.getConsumerLog().exception("consumerAction exception...")

    @abstractmethod
    def action(self):
        """
        消费生产者行为,
        有异常或者产生异常结果必须抛出ConsumberException
        :return:
        """
        pass

    @abstractmethod
    def success(self):
        """
        消费生产者行为成功后调用
        :return:
        """
        pass

    @abstractmethod
    def fail(self):
        """
        消费生产者行为失败后调用
        :return:
        """
        pass
