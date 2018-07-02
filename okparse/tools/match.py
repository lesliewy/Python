# -*- coding:utf-8 -*-

'''
下载指定ok_url_date的单场页面: http://www.okooo.com/danchang/180504
并解析，生成结果文件: match.dat

'''

from bs4 import BeautifulSoup
from download import persist
from utils import const
from files import file_util
import os
import logging
import re

# 日志
logging.basicConfig(filename=const.my_const.LOG_FILE, level=logging.INFO, format=const.my_const.LOG_FORMAT,
                    datefmt=const.my_const.DATE_FORMAT)


def download_persist(ok_url_date, replace=True):
    download_match(ok_url_date, replace)
    persist_match(ok_url_date, replace)


def download_match(ok_url_date, replace=True):
    match_term_dir = os.path.join(const.my_const.LOCAL_DATA_DIR, ok_url_date)
    file_util.create_dir(match_term_dir)

    match_file = os.path.join(match_term_dir, const.my_const.MATCH_HTML)
    if not replace and os.path.exists(match_file):
        return
    content = persist.persist_file(const.my_const.MATCH_URL_PRE + ok_url_date, match_file, "gbk", True)
    # 可能不存在
    if content.find("没有对阵") > 0:
        file_util.delete_dir(match_term_dir)

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


# 返回所有 match 信息.
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
            match_dict["hostGoals"] = strs[4]
            match_dict["visitingGoals"] = strs[5]
            match_dict["matchId"] = strs[6]
            matches.append(match_dict)
    return matches


def get_match_html(ok_url_date):
    match_dir = os.path.join(const.my_const.LOCAL_DATA_DIR, ok_url_date)
    return os.path.join(match_dir, const.my_const.MATCH_HTML)


def get_match_dat(ok_url_date):
    match_dir = os.path.join(const.my_const.LOCAL_DATA_DIR, ok_url_date)
    return os.path.join(match_dir, const.my_const.MATCH_DAT)


def __parse_match(filePath):
    logging.info("正在处理 " + filePath);
    f = open(filePath, 'r', encoding='utf-8')
    soup = BeautifulSoup(f, 'html5lib')  # html.parser   html5lib  lxml

    # 澳客期数
    ok_url_date = os.path.abspath(filePath).split("/")[-2]

    # 每天是一个table
    all_tables_soup = soup.select("#gametablesend > table")
    index = 0;
    lines = ""
    for table_soup in all_tables_soup:
        all_trs_soup = table_soup.select('tbody > tr.alltrObj')
        for tr_soup in all_trs_soup:
            index += 1
            logging.debug("正在处理 " + ok_url_date + " " + str(index))
            # 比赛id  tr的属性中没有, 从 欧 的url中取
            ok_match_id = tr_soup.select('> td.tdfx.td8 > a:nth-of-type(1)')[0].attrs['href'].split('/')[3]
            # 比赛名称
            match_name = tr_soup.select(' > td.td1.tdsx > a')[0].string
            # 比赛序号
            match_seq = tr_soup.select(' > td.td1.tdsx > span > i')[0].string
            # 比赛时间
            match_time = tr_soup.select(' > td.switchtime.timetd.td2')[0].attrs['title'].replace('比赛时间：', '')
            # 停售时间
            close_time = match_time[0:4] + '-' + tr_soup.select(' > td.switchtime.timetd.td2 > span')[0].string
            # 主队
            host_team_name = tr_soup.select(' > td.ztbox.overbg.td3 > a.sbg > span.homenameobj.homename')[0].string
            # 客队
            visiting_team_name = tr_soup.select(' > td.ztbox.overbg.td3 > a.fbg > span')[0].string
            # 主队进球数
            host_goals = tr_soup.select(' > td.tdfx.td6')[0].string.split('-')[0]
            # 客队进球数
            visiting_goals = tr_soup.select(' > td.tdfx.td6')[0].string.split('-')[1]

            # 格式化赋值.
            lines += '{matchSeq:5s} {matchName:10s} {hostTeamName:10s} {visitingTeamName:10s} {hostGoals:5s} {visitingGoals:5s} {matchId:10s}'.format(
                matchSeq=match_seq, matchName=match_name,
                hostTeamName=host_team_name, visitingTeamName=visiting_team_name, hostGoals=host_goals,
                visitingGoals=visiting_goals, matchId=ok_match_id) + "\n"
    return lines


def test_download_match():
    ok_url_date = "180504"
    download_match(ok_url_date)


def test_persist_match():
    persist_match('/Users/leslie/MyProjects/Data/Okooo/180504/match.html',
                  '/Users/leslie/MyProjects/Data/Okooo/180504/match.dat')


def test_get_match():
    get_match("/Users/leslie/MyProjects/Data/Okooo/180504/match.dat")

# test_download_match()
# test_persist_match()
# test_get_match()
