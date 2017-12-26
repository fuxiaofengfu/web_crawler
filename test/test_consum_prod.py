# -*- coding: utf-8 -*-
"""
    create 2017/12/25 15:13
    by xiaofengfu
"""
import log.common_log as log
import base.design.consumer.action as consumerAction
import base.design.productor.action as productorAction
import base.design.util.run_util as run_util


class ConsumberActionImpl(consumerAction.ConsumerAction):

    def __init__(self, action_str, params=None, try_num=0, max_try_num=0):
        super(ConsumberActionImpl, self).__init__(action_str, params, try_num, max_try_num)

    def action(self):
        log.getLogger().info("action......action=%s,params=%s" % (self.action_str, self.params))
        raise Exception(self.action_str)

    def success(self):
        log.getLogger().info("success......")

    def fail(self):
        log.getLogger().info("fail......")


class ProductorActionImpl(productorAction.ProductorAction):

    def __init__(self):
        super(ProductorActionImpl, self).__init__()

    def action(self):
        action_items = []
        for i in range(1, 2):
            action_str = "action__"+str(i)
            consumer_action = ConsumberActionImpl(action_str, max_try_num=3, try_num=0)
            action_items.append(consumer_action)
        return action_items


if __name__ == "__main__":
    action = ProductorActionImpl()
    run_util.Run(action, 5, 1, 1, 1).work_run()
