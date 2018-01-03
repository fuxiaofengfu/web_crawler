# -*- coding: utf-8 -*-
"""
    create 2018/1/3 20:05
    by xiaofengfu
"""
import os

import base.config.common_config as common_config
import crawler.util.common_util as common_util
import crawler.util.file_util as file_util


class Merge:

    def __init__(self):
        pass

    def mergeFile(self):
        crawler_path = common_config.CRAWLER_SAVE_PATH+os.sep+"done"
        dstr = "_".join(common_util.now().split(" "))
        file_path = common_config.CRAWLER_SAVE_PATH+os.sep+"merge"+os.sep+"crawler_"+dstr+".txt"
        file_util.mergeFile(crawler_path, file_path, False)


if __name__ == "__main__":
    Merge().mergeFile()
