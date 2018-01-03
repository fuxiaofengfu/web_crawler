# -*- coding: utf-8 -*-
"""
    create 2017/12/27 15:48
    by xiaofengfu

    排序工具类
    这里使用的是快速排序算法
"""


def fastSortDict(_dict):
    """
    因为字典类型是散列表的,所以对它的排序返回一个list
    [{key:value},{key:value},...]
    :param _dict:
    :return:
    """
    if not _dict:
        return _dict
    _list = _dict.keys()
    _list = fastSortList(_list)
    new_list = []
    for key in _list:
        new_list.append({key: _dict[key]})
    return new_list


def fastSortList(_list):
    """
    快速排序
    :param _list:
    :return:
    """
    if len(_list) <= 1:
        return _list
    tmp = _list.pop()
    small = [item for item in _list if tmp > item]
    big = [item for item in _list if tmp < item]
    return fastSortList(small) + [tmp] + fastSortList(big)
