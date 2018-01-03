# -*- coding: utf-8 -*-
"""
    create 2018/1/2 14:46
    by xiaofengfu
"""
import os
import shutil
import stat

import log.common_log as log


def mvFile(source_file, des_file):
    """
    将source_file移动到des_file
    :param source_file:
    :param des_file:
    :return:
    """
    try:
        shutil.move(source_file, des_file)
        return True
    except:
        log.getLogger().exception("mvFile exception ...")
    return False


def mergeFile(file_path, new_file, del_old=True):
    """
    将文件同级目录下的所有文件合并
    :param file_path:  要合并的文件目录的内容或者文件同级文件,必须有rw权限
    :param new_file: 合并产生的新文件
    :param del_old: 是否删除被合并的文件
    :return:
    """
    try:
        if os.path.isfile(file_path):
            file_path = os.path.dirname(file_path)

        if not os.path.isdir(file_path):
            raise Exception("不是目录:%s,请检查该路径是否是文件目录" % file_path)
        if not os.access(file_path, os.W_OK):
            raise Exception("文件目录:%s,不可写,请检查该目录是否可写" % file_path)
        if os.path.isdir(new_file):
            raise Exception("合并到的文件%s是目录，不能合并" % new_file)

        files = os.listdir(file_path)
        try:
            newfile = file(new_file, "a")
            while len(files) >= 1:
                f = files.pop()
                if f.startswith("."):  # 过滤掉隐藏文件
                    continue
                f = file_path + os.sep + f
                if not os.path.isfile(f):  # 过滤掉目录
                    continue
                if not os.access(f, os.W_OK):  # 文件不可写则忽略该文件
                    continue
                try:
                    _f = file(f, "r")
                    newfile.write(_f.read())
                    if del_old:
                        os.remove(f)  # 合并之后删除
                    os.chmod(f, stat.S_IRUSR)  # 改变该文件权限为只读模式,目的:已经合并的文件就不再重复合并
                except:
                    log.getLogger().exception("mergeFile ...")
                finally:
                    _f.close()
        except:
            log.getLogger().exception("mergeFile ...")
            return False
        finally:
            newfile.close()
    except:
        log.getLogger().exception("mergeFile ...")
        return False
    return True




