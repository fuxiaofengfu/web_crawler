# -*- coding: utf-8 -*-
"""
    create 2018/1/3 15:37
    by xiaofengfu
"""
from crawler.mycrawler import MyCrawler


def save_seed(url, title):
    """
    保存种子链接
    :param url:
    :param title:
    :return:
    """
    MyCrawler().saveSeedUrl(url, title)


if __name__ == "__main__":
    # 保存种子链接
    seed = "https://www.douban.com"
    save_seed(seed, "百度")
