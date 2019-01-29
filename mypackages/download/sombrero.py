import logging
import os

from bs4 import BeautifulSoup
from download import persist
from mystring import string_util

######################
#
# 解析文件组件.
#
######################


# 日志
LOG_FORMAT = "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename='sombrero.log', level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


###
#  获取beautiful soup
###
def get_soup(url, full_file_path):
    if (string_util.is_any_blank(url, full_file_path)):
        logging.error("url, full_file_path 都不能为空.");
        return;
    if (not os.path.isfile(full_file_path)):
        persist.persist_file(url, full_file_path);
    f = open(full_file_path, 'r', encoding='UTF-8')
    soup = BeautifulSoup(f, 'html5lib')  # html.parser   html5lib  lxml
    return f, soup


###
#  获取指定url、指定selector 下的文字.
###
def get_content_with_selector(soup, selector):
    if (string_util.is_any_blank(selector)):
        logging.error("selector 不能为空.")
        return;
    if (not soup):
        logging.error("soup 不能为空");
        return;
    result_list = soup.select(selector);
    result = "";
    if (result_list):
        result = result_list[0].string.strip()
    return result;


###
#  获取指定url、指定selector下指定类型标签的个数.
###
def get_num_of_child(soup, selector, child_type):
    logging.info("selector=%s, child_type=%s", selector, child_type);
    if (not soup):
        logging.error("soup 不能为空");
        return;
    selector = selector + " > " + child_type;
    result = len(soup.select(selector));
    return result;


###
#  获取指定url、指定selector下的text, 递归(目前只递归一次)
###
def get_content_recursion(soup, selector):
    logging.info("selector=%s", selector);
    if (not soup):
        logging.error("soup 不能为空");
        return;

    selector_list = soup.select(selector);
    if (not selector_list):
        logging.info("该selector不存在子节点");
        return;
    key_dict, concat_content = __get_content_from_list(selector_list);
    return key_dict, concat_content;


###
#  获取指定url、指定selector下的 dict, 通常是table 的表头.   dict: key: 序号(从0开始) , value: 表头.
###
def get_key(soup, selector):
    logging.info("selector=%s", selector);
    if (not soup):
        logging.error("soup 不能为空");
        return;
    key_dict, concat_content = get_content_recursion(soup, selector)
    return key_dict;


###
#  获取
###
def get_value(soup, selector, exclude_head=False, colume_key_dict={}):
    logging.info("selector=%s", selector)
    if (not soup):
        logging.error("soup 不能为空");
        return;
    value_list = soup.select(selector);
    if (not value_list):
        logging.info("该selector不存在子节点");
        return;
    value_dict = __get_value_dict(value_list, exclude_head, colume_key_dict);
    return value_dict

def __get_content_from_list(selector_list):
    concat_content = "";
    key_dict = {};
    i = 0;
    for e in selector_list:
        # e.text 可以取到子孙节点的text,然后拼接起来;  e.string 仅取当前节点;
        concat_content += e.text;
        key_dict[i] = e.text;
        i += 1;
    return key_dict, concat_content;


def __get_value_dict(selector_list, exclude_head, colume_key_dict):
    value_dict = {};
    i = 0;
    # 处理行
    for e in selector_list:
        if (exclude_head and i == 0):
            exclude_head = False;
            continue;
        # 处理行中列
        line = {};
        j = 0;
        for c in e.children:
            key_name = colume_key_dict.get(j);
            if (key_name):
                line[key_name] = c.text;
            else:
                line[j] = c.text;
            j += 1;
        value_dict[i] = line;
        i += 1;
    return value_dict
