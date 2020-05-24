"""
    从公众号号url文件中读取url，获取公众号内容，包括其中的图片，不包括视频。
    难点在获取图片，并将html中图片指向下载到本地的图片.

    整体过程:
       第一步: 获取所有文章的url
           1, Windows 电脑端打开待下载公众号的历史信息列表，下滑获取待下载的公众号文章;
           2, 右击查看源码，copy所有保存为 gzh_list.html
           另外，这一步做到自动化，可以参考: https://blog.csdn.net/shsongtao/article/details/96104865, https://www.jianshu.com/p/fe565169abec
           3, 使用 gen_gzh_urls 解析出所有的文章url 以及 日期, 保存到 gzh_urls.data, 内容格式为:20180104 title http:weixin.qq.com/.....

       第二步: 解析gzh_urls.data, 并下载文件, 包括其中的图片.
           1, 下载url指向的html;
           2, 解析html, 获取所有包含 data-src 属性的 <img>, 并下载图片;
           3, 去掉 <img> 中的 crossorigin 属性
           4, 更新html.

    下载视频方法:
        点击网页中的视频, 查看dev tools中的Network
        A: 存在Media 链接: 直接下载mp4。 url 类似:  https://ugcbsy.qq.com/uwMROfz2r5zCIaQXGdGnC2dfJ7xVXKbtPOti4lz6jGfpFpyW/t0636ltb2lf.p712.1.mp4?sdtfrom=v1104&guid=66ca4980ca1034f46896af106118d0db&vkey=5C4A3E409CB821FA74DB69BFAC2DEE09E3EE470BBCDEDFD43772925BEFFA64B1586EF0B46FB5BA9CBD4BB151A671B73738EC6ABC1B11AFA4F65EB81C4DA93EBE85006B621C5A2B0A7976111EE5A45C3ED9E66CA234AA17B94C2FAA9FC9E8663D399C38E0074A4209513FC6F44162EAAF5CA087904990C3192446A18CEE1A2487
           需要辨别广告的视频, 广告视频的url中通常有 p201.1.mp4

        B: 不存在Media 链接: 无法直接下载mp4.
           xhr 中有多段url 名称类似: 016_l06412yotcz.321002.1.ts,   017_l06412yotcz.321002.1.ts, 033_l06412yotcz.321002.1.ts, 这些就是视频流.
                               对应的url, 形如:  https://apd-be0c13e0bcddf434dcf46c5433ca1e0f.v.smtcdns.com/omts.tc.qq.com/AcsVhP4AdXV6vUcgLT6tgTtIyS4aloT5N8WCMLGLkXOQ/uwMROfz2r5zCIaQXGdGnC2df644Q3LWUuLvyGY4RMhgE_3T2/mjtAOVOu_-i-VqivMkhf8JXtII8HkboTg3vTs5Xxc_C5dNIrPiGP85EG4idaqgsSPQ4rEuXCpYhScAH8qPzs-ID0GS7IhpPkEQ3wCh8RslSQtznDQFVRLcXMIZUTgZ_X_dbJMixbKEmoivf0Um7jVdDWTy5wXsbnUQLyrxmIzJw/016_l06412yotcz.321002.1.ts?index=16&start=178360&end=191120&brs=12978392&bre=13769307&ver=4
           下载去掉参数的url, 例如上面的，下载url:  https://apd-be0c13e0bcddf434dcf46c5433ca1e0f.v.smtcdns.com/omts.tc.qq.com/AcsVhP4AdXV6vUcgLT6tgTtIyS4aloT5N8WCMLGLkXOQ/uwMROfz2r5zCIaQXGdGnC2df644Q3LWUuLvyGY4RMhgE_3T2/mjtAOVOu_-i-VqivMkhf8JXtII8HkboTg3vTs5Xxc_C5dNIrPiGP85EG4idaqgsSPQ4rEuXCpYhScAH8qPzs-ID0GS7IhpPkEQ3wCh8RslSQtznDQFVRLcXMIZUTgZ_X_dbJMixbKEmoivf0Um7jVdDWTy5wXsbnUQLyrxmIzJw/016_l06412yotcz.321002.1.ts
           如果是033_, 043_ 等较大的数字开头的，url最后的序号会有变化.
                                   例如，会变成  https://apd-be0c13e0bcddf434dcf46c5433ca1e0f.v.smtcdns.com/omts.tc.qq.com/AcsVhP4AdXV6vUcgLT6tgTtIyS4aloT5N8WCMLGLkXOQ/uwMROfz2r5zCIaQXGdGnC2df644Q3LWUuLvyGY4RMhgE_3T2/mjtAOVOu_-i-VqivMkhf8JXtII8HkboTg3vTs5Xxc_C5dNIrPiGP85EG4idaqgsSPQ4rEuXCpYhScAH8qPzs-ID0GS7IhpPkEQ3wCh8RslSQtznDQFVRLcXMIZUTgZ_X_dbJMixbKEmoivf0Um7jVdDWTy5wXsbnUQLyrxmIzJw/016_l06412yotcz.321002.2.ts
            下载的文件是ts格式, windows 下用狸窝转换器可以转成mp4.

    使用方法:
      1，按上面第一步来获取文章的源码 gzh_list.html
      2, 修改 gen_gzh_urls.py 的 main() 中的 article_list_html 的路径指向上一步中的gzh_list.html;
      3, 执行gen_gzh_urls_test.py 中的 test_main() 方法, 会自动分析，输出保存在gzh_urls.data
      4, 将之前公众号的文章保存在WX_GZH_DATA_DIR 指向的目录下，可以避免重复下载。  该目录下直接以年份开头.
      5, 执行 persist_gzh_test.py 中的 test_main() 下载文章及图片.


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
    logging.info("开始下载公众号文章...")
    persist_gzh_from_file(constants.WX_GZH_URL_FILE)


# 从已生成的文件中获取公众号url 和 日期, 来下载公众号里的文章.
def persist_gzh_from_file(gzh_url_file):
    if string_util.is_any_blank(gzh_url_file) or not os.path.exists(gzh_url_file):
        logging.error("文件未指定或指定的文件不存在: %s", gzh_url_file)
        return
    # 交互式提醒.
    if not can_persist_gzh():
        to_continue = input("存放公众号目录(" + constants.WX_GZH_DATA_DIR + ")非空, 确定是否继续(Y/N):")
        if not to_continue == 'Y':
            logging.info("存放公众号目录非空, 用户退出程序.")
            return
    lines = file_util.read_file(gzh_url_file, mode='L')
    num = 0
    num_of_html_download_total = 0
    num_of_img_download_total = 0
    for line in lines:
        if string_util.is_any_blank(line):
            continue
        article_date, title, url = line.split(constants.WX_GZH_URL_FILE_SEP)
        logging.info("正在处理: %s", article_date)
        html, html_download_flag = persist_gzh_html(url, article_date, title)
        if html_download_flag:
            num_of_html_download_total = num_of_html_download_total + 1

        # 下载图片，保存新的html
        soup = sombrero.get_soup_file(html)
        num_of_img_download = process_img(soup, article_date)
        num_of_img_download_total = num_of_img_download_total + num_of_img_download

        # 删除temp.html
        if html.endswith("/temp.html"):
            os.remove(html)

        num = num + 1
    logging.info("本次共处理了 %s 条记录, 其中下载html: %s 次, 下载图片: %s 次", num, num_of_html_download_total,
                 num_of_img_download_total)
    return


# 获取公众号文章html
def persist_gzh_html(url, article_date, title=None):
    if string_util.is_any_blank(url, article_date):
        logging.error('url 不能为空.')
        return

    # 新建目录
    article_dir = __create_dir__(article_date)

    download_flag = True
    # 已经存在同名html，则不再下载.
    temp_html_path = article_dir + 'temp.html'
    actural_html = article_dir + title + '.html'
    if os.path.exists(actural_html):
        download_flag = False
        return actural_html, download_flag

    persist.persist_file(url, temp_html_path)

    return temp_html_path, download_flag


# 下载图片，并修改html中<img> 添加 , 指向本地文件.
def process_img(soup, article_date):
    imgs = soup.find_all('img', attrs={"data-src": True})
    title = get_gzh_title(soup)
    # 新建目录，如: 2018/10
    article_dir, img_dir = __create_dir__(article_date, title)
    img_num = 0
    num_of_download = 0
    soup_changed = False
    for img in imgs:
        # 获取图片.
        img_url = img['data-src']
        if not img_url or not img_url.startswith('http'):
            continue
        img_file_name = '640_' + str(img_num)
        img_num = img_num + 1
        img_full_path = os.path.join(img_dir, img_file_name)
        if os.path.exists(img_full_path):
            continue
        try:
            persist.retrieve_by_url(img_url, img_full_path)
        except Exception as e:
            logging.error("存在异常，continue. %s", e)
            continue
        num_of_download = num_of_download + 1

        # html中添加src
        img['src'] = './' + img_dir.split('/')[-2] + '/' + img_file_name
        # 删除 crossorigin
        del img['crossorigin']
        soup_changed = True
    # 保存修改过的html
    if soup_changed:
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
# 日期格式 2019年9月18日
def __create_dir__(article_date, title=None):
    year = article_date[0:4]
    mon = article_date[5:article_date.index('月')].rjust(2, '0')
    full_path = constants.WX_GZH_DATA_DIR + year + '/' + mon + '/'
    if not os.path.exists(full_path):
        file_util.create_dir(full_path)
    if title:
        img_path = full_path + title + '/'
        if not os.path.exists(img_path):
            file_util.create_dir(img_path)
        return full_path, img_path
    return full_path
