### 从公众号列表html中解析url, article_date, title 并保存入文件.

import logging
import os
from download import sombrero
from files import file_util
from mystring import string_util

import constants

# 日志
LOG_FORMAT = "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename=constants.BASE_DIR + 'log/gzh.log', level=logging.INFO, format=LOG_FORMAT,
                    datefmt=DATE_FORMAT)


def main():
    article_list_html = '/Users/leslie/Work/Favorite/WX/金融/图解金融/图解金融201909-20200.html';
    parse_gzh_list_html(article_list_html)


def parse_gzh_list_html(file_path):
    if string_util.is_any_blank(file_path) or not os.path.exists(file_path):
        logging.error("文件不能为空或者文件不存在: %s", file_path)
        return None
    if not can_persist_gzh_url():
        to_continue = input("存放公众号文章url文件(wx/data/gzh_urls.data)非空, 确定是否继续(Y/N):")
        if not to_continue == 'Y':
            logging.info("存放公众号文章url文件非空, 用户退出程序.")
            return
    soup = sombrero.get_soup_file(file_path)
    article_tags = soup.find_all('div', attrs={"class": "weui_media_bd js_media"})
    articles = []
    num = 0
    for article_tag in article_tags:
        logging.debug("正在处理: %s", article_tag)
        h4_tag = article_tag.select('h4')
        if not h4_tag:
            continue
        url = h4_tag[0]['hrefs'].strip()
        title = h4_tag[0].contents[-1].strip()
        article_date = ''.join(article_tag.select('.weui_media_extra_info')[0].contents[0].strip())
        articles.append(constants.WX_GZH_URL_FILE_SEP.join((article_date, title, url)))
        num = num + 1
    file_util.write_lines(articles, constants.WX_GZH_URL_FILE, 'w')
    logging.info('共解析文章数: %s 条', num)
    return num


# 判断是否能够解析公众号文章url, 并保存为文件。 需要对应的文件是空的.
def can_persist_gzh_url():
    return os.path.exists(constants.WX_GZH_URL_FILE) and os.path.getsize(constants.WX_GZH_URL_FILE) <= 0
