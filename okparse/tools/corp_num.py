'''
   获取所有博彩公司的编号
   来源页面:
   欧赔: http://www.okooo.com/soccer/match/1000222/odds/ajax/?page=0&trnum=0&companytype=BaijiaBooks&type=0, 欧赔页面(http://www.okooo.com/soccer/match/1000222/odds/)是没有的.
   亚盘: 亚盘页面(http://www.okooo.com/soccer/match/1000222/ah/)是没有的.
'''
from download import persist
from bs4 import BeautifulSoup
from utils import const
from files import file_util
import os
import logging
import datetime
import json

# 日志
logging.basicConfig(filename=const.log.LOG_FILE, level=logging.INFO, format=const.log.LOG_FORMAT,
                    datefmt=const.log.DATE_FORMAT)

# 更新博彩公司编号信息.
def gen_corp_num_dat(match_id, ok_url_date):
    logging.info("正在生成博彩公司编号: " + ok_url_date + "   " + match_id)
    begin = datetime.datetime.now()
    # 先下载博彩公司赔率文件.
    downloadOdds(match_id, ok_url_date)

    # 获取博彩公司名称、编号dict
    corps_num_dict = __get_corp_num_dict(__get_dir(ok_url_date), match_id)

    # 与已有的编号文件合并;
    __merge_corp_num(corps_num_dict)

    end = datetime.datetime.now()
    logging.info("gen_corp_num_dat 执行总时间: " + str(end - begin))

# 下载的文件放入临时文件夹.
def downloadOdds(match_id, ok_url_date):
    url_date_dir = __get_dir(ok_url_date)
    file_util.create_dir(url_date_dir)

    headers = {"Referer": "http://www.okooo.com/soccer/match/1021841/odds/",
               "Cookie": "PHPSESSID=816c865d2d9ccb9141cb45ca88126c2a073bfd29; LastUrl=; __utmc=56961525; __utmz=56961525.1560151033.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1560151034; FirstOKURL=http%3A//www.okooo.com/danchang/; First_Source=www.okooo.com; pm=; IMUserID=9077087; IMUserName=abcdwy1; OkAutoUuid=67e3661bbc2745bcdc9a2453aff993b5; OkMsIndex=5; OKSID=816c865d2d9ccb9141cb45ca88126c2a073bfd29; M_UserName=%22abcdwy1%22; M_UserID=9077087; M_Ukey=77baf1ba6eb3e183bb03832b1db982ee; OkTouchAutoUuid=67e3661bbc2745bcdc9a2453aff993b5; OkTouchMsIndex=5; isInvitePurview=0; __utma=56961525.2121983609.1560151033.1560930306.1560930306.29; Hm_lpvt_5ffc07c2ca2eda4cc1c4d8e50804c94b=1560996973; __utmb=56961525.500.9.1561007176990",
               }

    odds_url_matchid_rep = const.my_const.ODDS_EMBEDED_TEMPLATE_URL.replace('{matchId}', str(match_id));
    for pageNum in range(0, 10):
        odds_url = odds_url_matchid_rep.replace('{pageNum}', str(pageNum));
        full_file_path = os.path.join(url_date_dir, match_id + "_" + str(pageNum) + ".dat")
        content = persist.get_response(odds_url, method="GET", encoding="utf8", withUserAgent=True, headers=headers)
        if (len(content) < 300):
            break;
        # 保存至本地文件.
        file_util.write_file(content, full_file_path, 'w')
        logging.info("下载文件完毕: " + full_file_path)

# 获取博彩公司编号信息
def get_corp_no():
    file_path = os.path.join(const.my_const.LOCAL_DATA_DIR, const.my_const.CORP_NO_FILE)
    if not os.path.exists(file_path):
        return
    return json.load(open(file_path, 'r'))

def __get_dir(ok_url_date):
    return os.path.join(const.my_const.LOCAL_DATA_DIR, ok_url_date + "/temp/corpNum")


# 解析所有文件, 获取到所有文件的dict
def __get_corp_num_dict(dir, match_id):
    corpNoDict = {}
    for parent, dirnames, filenames in os.walk(dir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:  # 输出文件信息
            if not filename.startswith(match_id):
                continue
            fullpath = os.path.join(parent, filename)
            logging.info("正在处理文件 " + fullpath)
            corpNoDict.update(__parseCorpNoAjax(fullpath))
    return corpNoDict


def __parseCorpNoAjax(filename):
    # 需要添加html 必须字段, 否则解析有问题.
    content = "<html><body><table> " + file_util.read_file(filename) + " </table></body></html>"
    soup = BeautifulSoup(content, 'html5lib')  # html.parser   html5lib  lxml
    all_tr_soup = soup.select("tr")

    corp_no_dict = {}
    for tr_soup in all_tr_soup:
        corp_name = tr_soup.attrs["data-pname"]
        logging.info("正在处理 " + str(corp_name))
        corp_no = tr_soup.attrs["id"][2:]
        corp_no_dict[corp_name] = corp_no
    return corp_no_dict


def __merge_corp_num(corps_num_dict):
    logging.info("本次共解析corpNo 个数: " + str(len(corps_num_dict)))
    existed_file_path = os.path.join(const.my_const.LOCAL_DATA_DIR, "corpNo.dat")
    if (os.path.exists(existed_file_path)):
        existed_dict = json.load(open(existed_file_path, 'r'))
        corps_num_dict.update(existed_dict)
    existed_file = open(existed_file_path, "w", encoding='utf-8')
    json.dump(corps_num_dict, existed_file, ensure_ascii=False, indent=4)
    logging.info(existed_file_path + " 已生成, 总个数: " + str(len(corps_num_dict)))
    return


gen_corp_num_dat("1005809", "180504");
