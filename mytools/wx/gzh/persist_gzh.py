"""
    从公众号号url文件中读取url，获取公众号内容，包括其中的图片。
    难点在获取图片，并将html中图片指向下载到本地的图片.

    整体过程:
       第一步: 获取所有文章的url
           1, Windows 电脑端打开待下载公众号的历史信息列表，下滑获取待下载的公众号文章;
           2, 右击查看源码，copy所有保存为 gzh_list.html
           3, 使用 shell/getURLFromjs.sh 从gzh_list.html 中解析出所有的文章url 以及 日期, 保存为 gzh_urls.data
       第二步: 解析gzh_urls.data, 并下载文件, 包括其中的图片.
           1,


"""
import logging
import os
from files import file_util
from download import persist
from mystring import string_util

import constants

# 日志
LOG_FORMAT = "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename=constants.BASE_DIR + 'log/gzh.log', level=logging.INFO, format=LOG_FORMAT,
                    datefmt=DATE_FORMAT)


# 获取公众号文章html
def persist_gzh_html(url):
    if string_util.is_any_blank(url):
        logging.error('url 不能为空.')
        return
    # 新建目录，如: 2018/10
    # TODO
    article_date = 20180120
    article_dir = __create_dir__(article_date)

    temp_html_path = article_dir + 'temp.html'
    persist.persist_file(url, temp_html_path)


# 下载图片，并修改html中<img> 添加 src, 指向本地文件.
def process_img(soup):
    imgs = soup.find_all('img', attrs={"data-src": True})
    # 新建目录，如: 2018/10
    # TODO
    article_date = 20180120
    article_dir = __create_dir__(article_date)
    img_num = 0
    for img in imgs:
        img_url = img['data-src']
        if not img_url:
            continue
        img_full_path = article_dir + '640' + str(img_num)
        persist.persist_file(img_url, img_full_path)
        img_num = img_num + 1



def get_gzh_title(soup):
    title = soup.select('#activity-name')
    if title:
        title = ''.join(title[0]).strip()
    else:
        title = 'untitled'
    return title

# TODO 日期格式可能需要修改
def __create_dir__(article_date):
    year = article_date[0:4]
    mon = article_date[4:6]
    full_path = constants.WX_GZH_DATA_DIR + year + '/' + mon + '/'
    if not os.path.exists(full_path):
        file_util.create_dir(full_path)
    return full_path
