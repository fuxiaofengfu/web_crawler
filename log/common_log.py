# -*- coding: utf-8 -*-
"""
    create 2017/12/22 19:02
    by xiaofengfu
    统一日志工具模块
"""
import logging
import logging.config as log_config
import yaml, os, sys


def getLogger(logger_name="normal_logger"):
    """
    提供给外部调用，统一创建日志方法,
    :param logger_name: 日志名称,
    可用参数值:consumer_logger,productor_logger,normal_logger
    :return: 返回日志对象
    """
    return logging.getLogger(logger_name)


__log_config_name = "log_config.yaml"
if __name__ == '__main__':
    __module_path = getattr(sys.modules['__main__'], '__file__', None)
else:
    __module_path = globals().get("__file__")
# __module_path = os.path.abspath(__file__)

__parent_path = os.path.split(__module_path)
__parent_path = os.path.dirname(__parent_path[0])
__log_config_file = __parent_path + os.sep + __log_config_name

try:
    __f = file(__log_config_file, "r")
    __config_data = yaml.safe_load(__f)
    log_config.dictConfig(__config_data)
finally:
    __f.close()
