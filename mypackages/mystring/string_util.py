# coding:utf-8

import logging

# 日志
LOG_FORMAT = "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename='string_utils.log', level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


# 从str中取出数字.
def get_num(value):
    if len(value) <= 0:
        return

    result = ""
    for j in value:
        if (j >= '0' and j <= '9') or j == '.':
            result += j
    return result


def a():
    html = "a/b/c.html"
    print(html.replace("\.html", "\.dat"))


def is_any_blank(*strs):
    logging.info("%s", strs);
    for s in strs:
        if (not s or len(str(s).strip()) == 0):
            return True;
    return False;