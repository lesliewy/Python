import json
import logging
import os
import time

from download import sombrero
from mystring import string_util

# 日志
LOG_FORMAT = "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename='parse.log', level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)

local_dir = "/Users/leslie/MyProjects/Data/Stock/report/";
url_lrb_t = "http://quotes.money.163.com/f10/lrb_{code}.html";
url_zcfzb_t = "http://quotes.money.163.com/f10/zcfzb_{code}.html";
url_xjllb_t = "http://quotes.money.163.com/f10/xjllb_{code}.html"

selector_lrb_column_key = "#scrollTable > div.col_r > table > tbody > tr";
selector_lrb_line_key = "#scrollTable > div.col_l > table > tbody > tr";
selector_lrb_value = "#scrollTable > div.col_r > table > tbody > tr";

selector_zcfzb_column_key = "#scrollTable > div.col_r > table > tbody > tr";
selector_zcfzb_line_key =  "#scrollTable > div.col_l > table > tbody > tr";
selector_zcfzb_value = "#scrollTable > div.col_r > table > tbody > tr";

def main():
    get_lrb("603220");


def get_lrb(code):
    logging.info("code = %s", code);
    if (string_util.is_any_blank(code)):
        logging.error("code 不能为空");
        return;
    type = "lrb";
    url_lrb = url_lrb_t.replace("{code}", code);
    html_full_path, json_full_path = __get_file_path(code, type);
    f, soup = sombrero.get_soup(url_lrb, html_full_path);

    colume_key_dict = sombrero.get_key(soup, selector_lrb_column_key, key_location="H", key_seq=0);
    line_key_dict = sombrero.get_key(soup, selector_lrb_line_key, key_location="V", key_seq=0);

    result = sombrero.get_value(soup, selector_lrb_value, exclude_top=True, colume_key_dict=colume_key_dict,
                                exclude_left=False, line_key_dict=line_key_dict)

    result_file = open(json_full_path, "w", encoding='utf-8')
    json.dump(result, result_file, ensure_ascii=False, indent=4)

    if (f):
        f.close();


def get_zcfzb(code):
    logging.info("code = %s", code);
    if (string_util.is_any_blank(code)):
        logging.error("code 不能为空");
        return;
    type = "zcfzb";
    url_zcfzb = url_zcfzb_t.replace("{code}", code);
    html_full_path, json_full_path = __get_file_path(code, type);
    f, soup = sombrero.get_soup(url_zcfzb, html_full_path);

    colume_key_dict = sombrero.get_key(soup, selector_zcfzb_column_key, key_location="H", key_seq=0);
    line_key_dict = sombrero.get_key(soup, selector_lrb_line_key, key_location="V", key_seq=0);

    result = sombrero.get_value(soup, selector_lrb_value, exclude_top=True, colume_key_dict=colume_key_dict,
                                exclude_left=False, line_key_dict=line_key_dict)

    result_file = open(json_full_path, "w", encoding='utf-8')
    json.dump(result, result_file, ensure_ascii=False, indent=4)

    if (f):
        f.close();


def __get_file_path(code, type):
    dir_date = time.strftime('%Y/%m/%d/', time.localtime());
    full_dir = os.path.join(local_dir , dir_date, type);
    if (not os.path.isdir(full_dir)):
        os.makedirs(full_dir);
    html_full_path = os.path.join(full_dir, type + "_" + code + ".html")
    json_full_path = html_full_path.replace(".html", ".json");
    return html_full_path, json_full_path


main()
