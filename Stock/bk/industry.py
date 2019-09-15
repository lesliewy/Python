"""
    行业板块 - 股票 对应关系
"""
import json
import logging
import os.path
import re
from typing import Dict
from typing import List

from download import persist
from files import file_util
from mystring import string_util

import Constants

# 日志
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename=Constants.LOG_PATH + "/" + 'industry.log', level=logging.INFO, format=LOG_FORMAT,
                    datefmt=DATE_FORMAT)

# 从此url获取所有的行业板块、概念板块名称.
sidemenu_json_url = 'http://quote.eastmoney.com/config/sidemenu.json'
# 从此url获取指定板块下的个股  pn: 页数, pz: 每页显示数, $$ 是板块代码,从sidemenu_json_url中获取
# pz 设为100， 最多取100只个股.
bk_stocks_url = "http://6.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112406913066009338764_1567918600091&pn=1&pz=100&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=b:$$&fields=f12,f14&_=1567918600092"


# 左侧菜单中沪深板块json, 是最原始的数据
def get_industry_notion_raw() -> Dict:
    resp_raw = persist.get_response(sidemenu_json_url, encoding="utf-8")
    # 去掉第一个字符，否则报错, 不知道第一个是什么
    resp_list = json.loads(resp_raw[1:])
    hsbk = list(filter(lambda n: n['title'] == '沪深板块', resp_list))[0]
    return hsbk


#
# 概念: {"key":"concept_board",
#         "next":[{"key":"boards2-90.BK0713","show":true,"name":"","title":"2025规划","href":"/center/boardlist.html#boards2-90.BK0713"}]
#      }
#
def get_industry_notion_json(bk_type: str) -> List:
    title = ''
    if bk_type == '行业':
        title = '行业板块'
    elif bk_type == '概念':
        title = '概念板块'
    else:
        logging.error('板块类型错误.')
        return None
    return list(filter(lambda n: n['title'] == title, get_industry_notion_raw()['next']))[0]


# 获取所有行业名称列表.  ["安防设备", "保险", "包装材料", "电力行业", ......]
def get_all_industries() -> List:
    industries = get_industry_notion_json('行业')
    return list(map(lambda n: n['title'], industries['next']))


# 获取所有概念名称列表. ["2025规划", "3D玻璃", "阿里概念", "北斗导航", ......]
def get_all_notions() -> List:
    notions = get_industry_notion_json('概念')
    return list(map(lambda n: n['title'], notions['next']))


# 根据板块代码, 获取该板块下的所有股票信息.
# [{"f12": "300247", "f13": 0, "f14": "三只松鼠"}, {"f12": "000868", "f13":0, "f14":"*ST安凯"}, ......]
def get_board_stocks(bk_code: str) -> List:
    if string_util.is_any_blank(bk_code):
        logging.error("bk_code 不能为空.")
        return None
    url = bk_stocks_url.replace('$$', bk_code)
    all_stocks_str = persist.get_response(url)
    if string_util.is_any_blank(all_stocks_str):
        return None
    # 正则获取需要的json字符串
    all_stocks_match = re.match('jQuery.*\\((.*)\\)', all_stocks_str)
    all_stocks_str_pruned = all_stocks_match.group(1)

    all_stocks_json = json.loads(all_stocks_str_pruned)
    if all_stocks_json["data"]:
        return all_stocks_json["data"]["diff"]
    return None


# 生成行业/概念板块的json信息
def get_board_json(all_bks):
    result = []
    for item in all_bks:
        one_json = {}
        bk_code = item["key"].split('.')[1]
        title = item["title"]
        stocks_info = get_board_stocks(bk_code)
        one_json["bk_code"] = bk_code
        one_json["title"] = title
        one_json["stocks"] = stocks_info
        result.append(one_json)
    return result


#  将行业/概念板块信息写入文件: industry.json, notion.json
def persist_boards_stocks():
    industry_json = get_industry_notion_json('行业')
    industry_bk_json = get_board_json(industry_json['next'])
    industry_json_file = Constants.DATA_PATH + '/' + 'industry.json'
    if not os.path.exists(industry_json_file):
        file_util.write_file(
            json.dumps(industry_bk_json, skipkeys=False, check_circular=True, sort_keys=False),
            industry_json_file,
            'w'
        )

    notion_json = get_industry_notion_json('概念')
    notion_bk_json = get_board_json(notion_json['next'])
    notion_json_file = Constants.DATA_PATH + '/' + 'notion.json'
    if not os.path.exists(notion_json_file):
        file_util.write_file(
            json.dumps(notion_bk_json, skipkeys=False, check_circular=True, sort_keys=False),
            notion_json_file,
            'w'
        )
