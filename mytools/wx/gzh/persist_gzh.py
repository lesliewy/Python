"""
    从公众号号url文件中读取url，获取公众号内容，包括其中的图片。
    难点在获取图片，并将html中图片指向下载到本地的图片.

    整体过程:
       第一步: 获取所有文章的url
           1, Windows 电脑端打开待下载公众号的历史信息列表，下滑获取待下载的公众号文章;
           2, 右击查看源码，copy所有保存为 gzh_list.html
           3, 使用 shell/getURLFromjs.sh 从gzh_list.html 中解析出所有的文章url 以及 日期, 保存为 gzh_urls.data, 内容格式为:20180104 http:weixin.qq.com/.....
       第二步: 解析gzh_urls.data, 并下载文件, 包括其中的图片.
           1, 下载url指向的html;
           2, 解析html, 获取所有包含 data-src 属性的 <img>, 并下载图片;
           3, 去掉 <img> 中的 crossorigin 属性
           4, 更新html.


"""
import logging
import os
from download import persist
from download import sombrero
from files import file_util
from mystring import string_util

import constants

# 日志
LOG_FORMAT = "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename=constants.BASE_DIR + 'log/gzh.log', level=logging.INFO, format=LOG_FORMAT,
                    datefmt=DATE_FORMAT)


# 主流程
def main():
    persist_gzh_from_file(constants.WX_GZH_URL_FILE)


# 从已生成的文件中获取公众号url 和 日期, 来下载公众号里的文章.
def persist_gzh_from_file(gzh_url_file):
    if string_util.is_any_blank(gzh_url_file) or not os.path.exists(gzh_url_file):
        logging.error("文件未指定或指定的文件不存在: %s", gzh_url_file)
        return
    '''
    if not can_persist_gzh():
        logging.error("请确保目标目录是空目录: %s", constants.WX_GZH_DATA_DIR)
        return
    '''
    lines = file_util.read_file(gzh_url_file, mode='L')
    num = 0
    num_of_download_total = 0
    for line in lines:
        if string_util.is_any_blank(line):
            continue
        article_date, url = line.split(' ')
        logging.info("正在处理: %s", article_date)
        temp_html = persist_gzh_html(url, article_date)

        # 下载图片，保存新的html
        soup = sombrero.get_soup_file(temp_html)
        num_of_download = process_img(soup, article_date)
        num_of_download_total = num_of_download_total + num_of_download

        # 删除temp.html
        os.remove(temp_html)

        num = num + 1
    logging.info("本次共处理了 %s 条记录, 其中下载图片: %s 次", num, num_of_download_total)
    return


# 获取公众号文章html
def persist_gzh_html(url, article_date):
    if string_util.is_any_blank(url, article_date):
        logging.error('url 不能为空.')
        return
    # 新建目录
    article_dir = __create_dir__(article_date)

    temp_html_path = article_dir + 'temp.html'
    persist.persist_file(url, temp_html_path)

    return temp_html_path


# 下载图片，并修改html中<img> 添加 , 指向本地文件.
def process_img(soup, article_date):
    imgs = soup.find_all('img', attrs={"data-src": True})
    title = get_gzh_title(soup)
    # 新建目录，如: 2018/10
    article_dir, img_dir = __create_dir__(article_date, title)
    img_num = 0
    num_of_download = 0
    for img in imgs:
        # 获取图片.
        img_url = img['data-src']
        if not img_url:
            continue
        img_file_name = '640_' + str(img_num)
        img_num = img_num + 1
        img_full_path = os.path.join(img_dir, img_file_name)
        if os.path.exists(img_full_path):
            continue
        persist.retrieve_by_url(img_url, img_full_path)
        num_of_download = num_of_download + 1

        # html中添加src
        img['src'] = './' + img_dir.split('/')[-2] + '/' + img_file_name
        # 删除 crossorigin
        del img['crossorigin']
    # 保存修改过的html
    html_file_path = os.path.join(article_dir, title + '.html')
    sombrero.persist_soup(soup, html_file_path)
    return num_of_download


# 解析公众号html获取标题.
def get_gzh_title(soup):
    title = soup.select('#activity-name')
    if title:
        title = ''.join(title[0]).strip()
    else:
        title = 'untitled'
    return title


# 判断是否能够下载公众号文章。 需要对应的目录下是空的.
def can_persist_gzh():
    return os.path.exists(constants.WX_GZH_DATA_DIR) and not os.listdir(constants.WX_GZH_DATA_DIR)


# 新建文章目录，至月份; 如果传入title, 同时新建文章同名目录，用于存放该篇文章图片.
# TODO 日期格式可能需要修改
def __create_dir__(article_date, title=None):
    year = article_date[0:4]
    mon = article_date[4:6]
    full_path = constants.WX_GZH_DATA_DIR + year + '/' + mon + '/'
    if not os.path.exists(full_path):
        file_util.create_dir(full_path)
    if title:
        img_path = full_path + title + '/'
        if not os.path.exists(img_path):
            file_util.create_dir(img_path)
        return full_path, img_path
    return full_path
