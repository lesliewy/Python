# -*- coding:utf-8 -*-

'''
下载指定ok_url_date的单场页面: http://www.okooo.com/danchang/180504
并解析，生成结果文件: match.dat,  格式为:
比赛序号  联赛名称  主队  客队  比赛日期 主队得分  客队得分 比赛结果  match_id

'''
import logging
import os
import re
from bs4 import BeautifulSoup
from download import persist
from files import file_util
from mystring import string_util

from utils import const
from utils import match_utils

# 日志
logging.basicConfig(filename=const.log.LOG_FILE, level=logging.INFO, format=const.log.LOG_FORMAT,
                    datefmt=const.log.DATE_FORMAT)


# 主流程.  date_range: 19 将会下载2019年所有的match.html; 190503: 将会下载ok_url_date = 190503 期的match.html;
def main(date_range):
    download_persist(date_range, replace_match_html=False, replace_match_dat=True)


def download_persist(date_range, replace_match_html=True, replace_match_dat=True):
    # 处理一年数据.
    num_of_html_download = 0;
    if len(date_range) == 2:
        for i in range(1, 13):
            mon = str(i).rjust(2, '0')
            for j in range(1, 10):
                term = str(j).rjust(2, '0')
                ok_url_date = date_range + mon + term
                actural_download_flag, has_matches = download_match(ok_url_date, replace_match_html)
                # 如果没有对阵，直接跳出该循环，进入下一个月.
                if not has_matches:
                    break;
                persist_match(ok_url_date, replace_match_dat)
                if actural_download_flag:
                    num_of_html_download = num_of_html_download + 1

    elif len(date_range) == 6:
        actural_download_flag, has_matches = download_match(date_range, replace_match_html)
        if not has_matches:
            logging.info("全部处理完成, 该ok_url_date没有比赛.")
            return;
        persist_match(date_range, replace_match_dat)
        if actural_download_flag:
            num_of_html_download = num_of_html_download + 1
    logging.info("全部处理完成，本次共下载match.html %s 次", num_of_html_download)


# 根据日期来下载match.html
def download_match(ok_url_date, replace=True):
    match_term_dir = os.path.join(const.my_const.LOCAL_DATA_DIR, ok_url_date)
    file_util.create_dir(match_term_dir)

    actural_download_flag = True
    has_matches = True
    match_file = os.path.join(match_term_dir, const.my_const.MATCH_HTML)
    if not replace and os.path.exists(match_file):
        actural_download_flag = False
        has_matches = True
        return actural_download_flag, has_matches
    content = persist.persist_file(const.my_const.MATCH_URL_PRE + ok_url_date, match_file, "gbk", True)
    # 可能不存在
    if content.find("没有对阵") > 0:
        file_util.delete_dir(match_term_dir)
        actural_download_flag = False
        has_matches = False
        return actural_download_flag, has_matches
    return actural_download_flag, has_matches


# 根据日期，来解析该日期的match.html, 并将结果存入match.dat
def persist_match(ok_url_date, replace=True):
    html_path = get_match_html(ok_url_date)
    if not os.path.exists(html_path):
        return
    dat_path = get_match_dat(ok_url_date)
    if not replace and os.path.exists(dat_path):
        return
    content = __parse_match(html_path)
    # 当下载的html中没有数据时, 无须生成dat.
    if len(content) <= 1:
        return
    file_util.write_file(content, dat_path, 'w')


# 从match.dat中获取所有 match 信息.
def get_match(ok_url_date):
    full_match_dat = get_match_dat(ok_url_date)
    if not os.path.exists(full_match_dat):
        logging.error(full_match_dat + " not exists.")
        return;
    matches = []
    with open(full_match_dat) as f:
        for line in f.readlines():
            match_dict = {}
            strs = re.split(" +", line)
            # 存在列数不足的情况. 比如比赛延期导致没有比分等
            if len(strs) <= 7:
                continue
            match_dict["matchSeq"] = strs[0]
            match_dict["leagueName"] = strs[1]
            match_dict["hostName"] = strs[2]
            match_dict["visitingName"] = strs[3]
            match_dict["matchTime"] = strs[4]
            match_dict["hostGoals"] = strs[5]
            match_dict["visitingGoals"] = strs[6]
            match_dict["matchResult"] = strs[7]
            match_dict["matchId"] = strs[8]
            matches.append(match_dict)
    return matches


# match.html 本地绝对路径.
def get_match_html(ok_url_date):
    match_dir = os.path.join(const.my_const.LOCAL_DATA_DIR, ok_url_date)
    return os.path.join(match_dir, const.my_const.MATCH_HTML)


# match.dat 本地绝对路径
def get_match_dat(ok_url_date):
    match_dir = os.path.join(const.my_const.LOCAL_DATA_DIR, ok_url_date)
    return os.path.join(match_dir, const.my_const.MATCH_DAT)


# 解析match.html
def __parse_match(filePath):
    logging.info("正在处理 " + filePath);
    f = open(filePath, 'r', encoding='utf-8')
    soup = BeautifulSoup(f, 'html5lib')  # html.parser   html5lib  lxml
    f.close()

    # 澳客期数
    ok_url_date = os.path.abspath(filePath).split("/")[-2]

    # 每天是一个table
    all_tables_soup = soup.select("#gametablesend > table")
    index = 0;
    lines = ""
    default_when_missing = '-'
    for table_soup in all_tables_soup:
        all_trs_soup = table_soup.select('tbody > tr.alltrObj')
        for tr_soup in all_trs_soup:
            index += 1
            logging.debug("正在处理 " + ok_url_date + " " + str(index))
            # 比赛id  tr的属性中没有, 从 欧 的url中取
            ok_match_id = __process_missing__(
                tr_soup.select('> td.tdfx.td8 > a:nth-of-type(1)')[0].attrs['href'].split('/')[3], default_when_missing)
            # 比赛名称
            match_name = __process_missing__(tr_soup.select(' > td.td1.tdsx > a')[0].string, default_when_missing)
            # 比赛序号
            match_seq = __process_missing__(tr_soup.select(' > td.td1.tdsx > span > i')[0].string, default_when_missing)
            # 比赛时间
            match_time = __process_missing__(
                tr_soup.select(' > td.switchtime.timetd.td2')[0].attrs['title'].replace('比赛时间：', ''),
                default_when_missing)
            # 停售时间
            close_time = __process_missing__(
                match_time[0:4] + '-' + tr_soup.select(' > td.switchtime.timetd.td2 > span')[0].string,
                default_when_missing)
            # 主队
            host_team_name = __process_missing__(
                tr_soup.select(' > td.ztbox.overbg.td3 > a.sbg > span.homenameobj.homename')[0].string,
                default_when_missing)
            # 客队
            visiting_team_name = __process_missing__(tr_soup.select(' > td.ztbox.overbg.td3 > a.fbg > span')[0].string,
                                                     default_when_missing)
            # 主队进球数
            host_goals = __process_missing__(tr_soup.select(' > td.tdfx.td6')[0].string.split('-')[0],
                                             default_when_missing)
            # 客队进球数
            visiting_goals = __process_missing__(tr_soup.select(' > td.tdfx.td6')[0].string.split('-')[1],
                                                 default_when_missing)
            # 比赛结果
            match_result = __process_missing__(match_utils.get_match_result(host_goals, visiting_goals),
                                               default_when_missing)

            # 格式化赋值. ">" 表示右对齐
            lines += '{matchSeq:>5s},{matchName:>10s},{hostTeamName:>10s},{visitingTeamName:>10s},{matchTime:>25s},{hostGoals:>5s},{visitingGoals:>5s},{matchResult:>5s},{matchId:>10s}'.format(
                matchSeq=match_seq, matchName=match_name,
                hostTeamName=host_team_name, visitingTeamName=visiting_team_name, matchTime=match_time,
                hostGoals=host_goals,
                visitingGoals=visiting_goals, matchResult=match_result, matchId=ok_match_id) + "\n"
    logging.info("处理完毕.")
    return lines


def __process_missing__(value, default_value):
    if string_util.is_any_blank(value):
        return default_value
    return value
