'''
获取博彩公司开出的欧赔, 包含所有赔率数据: http://www.okooo.com/soccer/match/1022465/odds/change/82/
并解析，生成结果文件.
'''
import logging
import os

from bs4 import BeautifulSoup
from download import persist
from files import file_util
from mystring import string_util

from utils import const

EURO_ODDS_ALL_TEMPLATE_URL = "http://www.okooo.com/soccer/match/{matchId}/odds/change/{corpNo}/"

# 日志
logging.basicConfig(filename=const.my_const.LOG_FILE, level=logging.INFO, format=const.my_const.LOG_FORMAT,
                    datefmt=const.my_const.DATE_FORMAT)


# 下载并解析某家博彩公司的欧赔数据.
def download_persist(ok_url_date, match_id, corp_no, match_seq=None, replace=False):
    existed = download_euro_odds_all(ok_url_date, match_id, corp_no, match_seq, replace)
    if existed:
        return existed
    existed = persist_euro_odds_all(ok_url_date, match_id, corp_no, match_seq, replace)
    return existed


# 下载某家博彩公司的欧赔信息, html 文件.
def download_euro_odds_all(ok_url_date, match_id, corp_no, match_seq=None, replace=False):
    url = EURO_ODDS_ALL_TEMPLATE_URL.replace("{matchId}", match_id).replace("{corpNo}", corp_no);
    full_file_parent = __get_euro_odds_dir(ok_url_date)
    file_util.create_dir(full_file_parent)
    full_file = __get_euro_odds_html_path(ok_url_date, match_id, corp_no, match_seq)

    headers = __build_header()
    if not replace and os.path.exists(full_file):
        return True
    persist.persist_file(url, full_file, encoding="gbk", withUserAgent=True, headers=headers, method='GET')


# 解析某家博彩公司的欧赔信息, 并生成结果文件, dat 文件.
def persist_euro_odds_all(ok_url_date, match_id, corp_no, match_seq=None, replace=False):
    existed = False
    dat_path = __get_euro_odds_dat_path(ok_url_date, match_id, corp_no, match_seq);
    if not replace and os.path.exists(dat_path):
        existed = True
        return existed
    content = __parse_euro_odds_all(__get_euro_odds_html_path(ok_url_date, match_id, corp_no, match_seq))
    # 当下载的html中没有数据时, 无须生成dat.
    if len(content) <= 1:
        return existed
    file_util.write_file(content, dat_path, 'w')
    return existed


def __build_header():
    header = {"Referer": "http://www.okooo.com/soccer/match/1021841/odds/",
              "Cookie": "LastUrl=; __utmc=56961525; __utmz=56961525.1528613715.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1528613716; FirstOKURL=http%3A//www.okooo.com/danchang/; First_Source=www.okooo.com; PHPSESSID=3066e165eae588bbf6fa9e57acb5e615095e4bd6; OkAutoUuid=7159b688a7318d84d715696732bee028; OkMsIndex=4; isInvitePurview=0; IMUserID=9077087; IMUserName=abcdwy1; DRUPAL_LOGGED_IN=Y; UWord=d461d8cd987f00b204e9800998ecf84727e; __utma=56961525.109803555.1528613715.1529733295.1529735348.8; Hm_lpvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1529736243; __utmb=56961525.7.8.1529736243418",
              }
    return header


def __get_euro_odds_dir(ok_url_date):
    return os.path.join(const.my_const.LOCAL_DATA_DIR, ok_url_date, "corpEuroOdds")


def __get_euro_odds_html_path(ok_url_date, match_id, corp_no, match_seq=None):
    match_seq_pre = ""
    if match_seq:
        match_seq_pre = match_seq + "_"
    return os.path.join(__get_euro_odds_dir(ok_url_date), match_seq_pre + match_id + "_" + corp_no + ".html")


def __get_euro_odds_dat_path(ok_url_date, match_id, corp_no, match_seq=None):
    return __get_euro_odds_html_path(ok_url_date, match_id, corp_no, match_seq).replace(".html", ".dat")


def __parse_euro_odds_all(file_path):
    logging.info("正在处理 " + file_path);
    f = open(file_path, 'r', encoding='utf-8')
    soup = BeautifulSoup(f, 'html5lib')  # html.parser   html5lib  lxml
    lines = ""

    all_trs = soup.select("body > div.wrap > table > tbody > tr")
    for tr in all_trs:
        # 存在没有 <td> 的情况.
        all_tds = tr.select("td")
        if (not all_tds):
            continue
        # 存在不是时间的.
        odds_time_temp1 = all_tds[0].string
        if odds_time_temp1 == None:
            continue
        odds_time_temp2 = all_tds[0].string.strip()
        if (not odds_time_temp2.startswith("2")):
            continue

        # 时间
        odds_time = odds_time_temp2[0:16]
        # 更新
        odds_update_time_temp = all_tds[1].string.strip()
        odds_update_time = odds_update_time_temp.replace("赛前", "").replace("小时", ".").replace("分", "")
        # 赔率-主
        odds_host = string_util.get_num(all_tds[2].string.strip())
        # 赔率-平
        odds_even = string_util.get_num(all_tds[3].string.strip())
        # 赔率-负
        odds_visiting = string_util.get_num(all_tds[4].string.strip())
        # 概率-主
        prob_host = string_util.get_num(all_tds[5].string.strip())
        # 概率-平
        prob_even = string_util.get_num(all_tds[6].string.strip())
        # 概率-负
        prob_visiting = string_util.get_num(all_tds[7].string.strip())
        # 凯利指数-主
        kelly_host = string_util.get_num(all_tds[8].string.strip())
        # 凯利指数-平
        kelly_even = string_util.get_num(all_tds[9].string.strip())
        # 凯利指数-负
        kelly_visiting = string_util.get_num(all_tds[10].string.strip())
        # 赔付率
        compensate = string_util.get_num(all_tds[11].string.strip())

        # 格式化赋值.
        lines += '{oddsTime:30s} {oddsUpdateTime:10s} {oddsHost:7s} {oddsEven:7s} {oddsVisiting:7s} {probHost:10s} {probEven:10s} {probVisiting:10s} {kellyHost:7s} {kellyEven:7s} {kellyVisiting:7s} {compensate:7s}'.format(
            oddsTime=odds_time, oddsUpdateTime=odds_update_time, oddsHost=odds_host, oddsEven=odds_even,
            oddsVisiting=odds_visiting,
            probHost=prob_host, probEven=prob_even, probVisiting=prob_visiting,
            kellyHost=kelly_host, kellyEven=kelly_even, kellyVisiting=kelly_visiting, compensate=compensate) + "\n"
    return lines

# download_euro_odds_all("180504", "1022465", "82")
# persist_euro_odds_all("/Users/leslie/MyProjects/Data/Okooo/180504/corpEuroOdds/1022465_82.html",
#                      "/Users/leslie/MyProjects/Data/Okooo/180504/corpEuroOdds/1022465_82.dat")
