# -*- coding: utf-8 -*-
"""
    create 2017/12/22 19:02
    by xiaofengfu
"""
import logging
import logging.config as log_config
import yaml, os, sys

log_config_name = "log_config.yaml"
if __name__ == '__main__':
    module_path = getattr(sys.modules['__main__'], '__file__', None)
else:
    module_path = globals().get("__file__")
# module_path = os.path.abspath(__file__)

parent_path = os.path.split(module_path)
parent_path = os.path.dirname(parent_path[0])
log_config_file = parent_path + os.sep + log_config_name

try:
    f = file(log_config_file, "r")
    config_data = yaml.safe_load(f)
    log_config.dictConfig(config_data)
finally:
    f.close()


def getLogger(logger_name="normal_logger"):
    return logging.getLogger(logger_name)
