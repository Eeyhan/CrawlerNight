#!usr/bin/env python
# -*- coding:utf-8 -*-


from conf.settings import *


def logger():
    # 创建一个文件型日志对象
    log_file = '%s/logs/%s' % (BASE_DIR, LOG_PATH)
    fh = logging.FileHandler(log_file)
    fh.setLevel(LOG_LEVEL)

    # # 创建一个输出到屏幕型日志对象
    # sh = logging.StreamHandler()
    # sh.setLevel(LOG_LEVEL)

    # 设置日志格式
    formater = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # 添加格式到文件型和输出型日志对象中
    fh.setFormatter(formater)
    # sh.setFormatter(formater)

    # 创建log对象，命名
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)

    # 把文件型日志和输出型日志对象添加进logger
    logger.addHandler(fh)
    # logger.addHandler(sh)
    return logger
