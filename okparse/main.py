from utils import const
from tools import corp_euro_odds, match, corp_num
import os
import logging
import time

# 日志
logging.basicConfig(filename=const.my_const.LOG_FILE, level=logging.INFO, format=const.my_const.LOG_FORMAT,
                    datefmt=const.my_const.DATE_FORMAT)

corp_names = ["立博", "Bet365"]


def process(ok_url_date):
    # 下载并处理match.html, 生成match.dat
    match.download_persist(ok_url_date, False)
    match_persist_path = match.get_match_dat(ok_url_date)
    if not os.path.exists(match_persist_path):
        logging.error(match_persist_path + " not exists.")
        return

    corps_no = corp_num.get_corp_no()
    if not corps_no or len(corps_no) == 0:
        logging.error("博彩公司编号文件不存在. return now...")
        return

    # 遍历match
    matches = match.get_match(ok_url_date)
    for corp_name in corp_names:
        corp_no = corps_no[corp_name]
        for match_dict in matches:
            match_seq = match_dict["matchSeq"]
            match_id = match_dict["matchId"]
            logging.info(
                "正在处理 ok_url_date=" + ok_url_date + " corp_name=" + corp_name + "  match_seq=" + match_seq + " match_id=" + match_id)
            # 下载指定博彩公司的欧赔数据.
            existed = corp_euro_odds.download_persist(ok_url_date, match_id, corp_no, match_seq, False)
            # 已经存在的文件，不需要延时.
            if not existed:
                time.sleep(2)


# process("180509")

# 处理年、月的比赛数据.
def process_batch(year, month=None):
    if len(year) != 2 or (month != None and len(month) != 2):
        logging.error("年份、月份必须是2位.")
        return
    if month:
        for seq in range(1, 10):
            ok_url_date = year + month + str(seq).rjust(2, "0")
            process(ok_url_date)
    else:
        for month_temp in range(1, 13):
            for seq in range(1, 10):
                if seq >= 10:
                    break
                ok_url_date = year + str(month_temp).rjust(2, "0") + str(seq).rjust(2, "0")
                try:
                    process(ok_url_date)
                except Exception as e:
                    continue

# 下载文件.
# process_batch("16")
# process_batch("18", "06")
