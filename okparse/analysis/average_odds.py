"""
    99家平均欧赔数据分析.

"""
import logging
import numpy as np
import os
from mystring import string_util

from utils import const

# 日志
logging.basicConfig(filename=const.log.LOG_FILE, level=logging.INFO, format=const.log.LOG_FORMAT,
                    datefmt=const.log.DATE_FORMAT)


def get_data_from_match_dat(match_dat_file):
    if string_util.is_any_blank(match_dat_file) or not os.path.exists(match_dat_file):
        logging.error("未指定match.dat文件，或指定的文件不存在: %s", match_dat_file)
        return None
    headers = 'league_name, host_name, visiting_name, match_time, host_goals, visiting_goals, match_result, match_id'
    return np.genfromtxt(fname=match_dat_file, usecols=(1, 2, 3, 4, 5, 6, 7, 8), names=headers, dtype=('<U20', '<U20', '<U20', '<U20', '<i2', '<i2', '<U2', '<U8'),
                         autostrip=True, delimiter=',')
