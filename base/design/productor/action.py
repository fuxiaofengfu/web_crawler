# -*- coding: utf-8 -*-
"""
    create 2017/12/24 11:59
    by xiaofengfu
"""
import base.exception.productor_exception as pro_exception


class ProductorAction(object):

    def __init__(self):
        pass

    def action(self):
        """
        产生消费者行为,返回消费者列表
        这里是另一种处理类似抽象方法的实现
        定义一个异常方法,要求子类必须重写该方法,否则抛出生产者异常
        :return:
        """
        raise pro_exception.ProductorException("productor exception.....")
