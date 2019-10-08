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


def get_data_from_match_dat(match_dat_file, exclude_unopen=True):
    if string_util.is_any_blank(match_dat_file) or not os.path.exists(match_dat_file):
        logging.error("未指定match.dat文件，或指定的文件不存在: %s", match_dat_file)
        return None
    headers = 'league_name, host_name, visiting_name, match_time, host_goals, visiting_goals, match_result, match_id'
    result = np.genfromtxt(fname=match_dat_file, usecols=(1, 2, 3, 4, 5, 6, 7, 8), names=headers,
                           dtype=(['<U20', '<U20', '<U20', '<U20', '<i2', '<i2', '<U2', '<U8']),
                           missing_values={4: '-1'},
                           filling_values={4: -2},
                           autostrip=True, delimiter=',')
    if exclude_unopen:
        result = np.delete(result, np.where(result[:]['host_goals'] < 0), axis=0)
    return result


def desc(match_dat_file):
    mat = get_data_from_match_dat(match_dat_file, exclude_unopen=True)
    result = "===== 概述:\n"

    result = result + "--- 比赛场次: " + str(mat.size) + "\n"

    max_host_goals = np.max(mat[:]["host_goals"])
    max_host_goals_info = mat[np.where(mat[:]['host_goals'] == max_host_goals)]
    result = result + "--- 主队进球最多的比赛: " + str(max_host_goals_info) + "\n"

    max_visiting_goals = np.max(mat[:]['visiting_goals'])
    max_visiting_goals_info = mat[np.where(mat[:]['visiting_goals'] == max_visiting_goals)]
    result = result + "--- 客队进球最多的比赛: " + str(max_visiting_goals_info) + "\n"

    # 水平拼接两个ndarray
    nrows = mat.shape[0]
    mat_goals = np.hstack((mat[:]['host_goals'].reshape(nrows, 1), mat[:]['visiting_goals'].reshape(nrows, 1)))
    diff_goals = np.abs(np.diff(mat_goals))
    max_diff_goals = np.max(diff_goals)
    max_diff_goals_info = mat[np.where(diff_goals == max_diff_goals)[0]]
    result = result + "--- 分差最多的比赛: " + str(max_diff_goals_info) + "\n"

    logging.info(result)
