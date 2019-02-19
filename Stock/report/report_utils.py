import logging

from db import mongo
from mystring import string_util

# mongodb 连接
dbname = "stock";
username = "stock"
password = "stock123"
db = mongo.get_mongo_db(dbname, username, password);


def trans_money(*strs):
    result = ()
    for s in strs:
        if s.find('--') > -1:
            result += (s,)
        else:
            result += (int(s.replace(',', '')),)
    return result


def get_latest_season_date(year, mon):
    result = ""
    if mon >= 1 and mon <= 3:
        result = str(year - 1) + "1231"
    elif mon >= 4 and mon <= 6:
        result = str(year) + "0331"
    elif mon >= 7 and mon <= 9:
        result = str(year) + "0630"
    elif mon >= 10 and mon <= 12:
        result = str(year) + "0930"
    return result


def get_last_season_date(season_date):
    year = int(season_date[0:4])
    month_day = season_date[4:8]
    result = ""
    if month_day == "0331":
        result = str(year - 1) + "1231"
    elif month_day == "0630":
        result = str(year) + "0331"
    elif month_day == "0930":
        result = str(year) + "0630"
    elif month_day == "1231":
        result = str(year) + "0930"
    return result


# 同比， 计算去年同期的report_date
def get_last_year_report_date(report_date):
    if not str(report_date).isdigit():
        return None
    return str(int(report_date[0:4]) - 1) + report_date[4:8]


def get_one_record_dict(collection_name, code):
    if (string_util.is_any_blank(collection_name, code)):
        logging.error("collection_name, code 不能为空.");
        return;
    record = list(db[collection_name].find({"code": code}))
    return dict(record[0]) if record and len(record) > 0 else None
