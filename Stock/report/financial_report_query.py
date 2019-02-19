import time

from mystring import string_util
from myutils import common_util

from Stocks import *
from report import financial_report_statistics
from report import report_utils

# 日志

LOG_FORMAT = "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename='../log/query.log', level=logging.INFO, format=LOG_FORMAT,
                    datefmt=DATE_FORMAT)

# 一条记录
lrb_dict, xjllb_dict, zcfzb_dict = None, None, None


###############################
#
#  异常点:
#    摸鱼小组 2019-01-24
#
#
###############################


def query_one(code, report_date_type, num_of_report):
    logging.info("code=%s, name=%s", code, Stocks.get_name_by_code(code))
    if (string_util.is_any_blank(code)):
        logging.error("code 不能为空.")
        return;
    if (not assign_dict(code)):
        return;

    xj_report = cal_report(report_date_type, "现金", num_of_report)

    fz_report = cal_report(report_date_type, "负债", num_of_report)

    # 存货, 固定资产, 固定资产/总资产, 固定资产构成没法获取，不然可以查看其中房地产占比.
    gdzc_report = cal_report(report_date_type, "固定资产、存货", num_of_report)

    sy_report = cal_report(report_date_type, "商誉", num_of_report)

    # 盈利能力: 营业收入(可惜没法获取其构成,看看主营收入占比)销售净利率(%)    营运能力: 总资产周转率(次)
    ylnl_report = cal_report(report_date_type, "盈利能力", num_of_report)
    ylnl_report_tb = cal_report(report_date_type, "盈利能力", num_of_report, tb="Y")

    logging.info(xj_report + fz_report + gdzc_report + sy_report + ylnl_report + ylnl_report_tb)


def query_statistics(report_date, selected_codes={}):
    start = time.time()
    if (string_util.is_any_blank(report_date)):
        logging.error("report_date 不能为空.")
        return;
    # 资产负债率排名
    zcfzl_dict = financial_report_statistics.cal_fz_zc(report_date, selected_codes=selected_codes, reverse=True)
    logging.info("\n%s 资产负债率\n%s", report_date, common_util.format_table_dict(zcfzl_dict, 10))
    end = time.time()
    logging.info("统计耗时: %s s", (end - start))


# ===================================================================================================

# tb: 是否是同比数据, 同比计算是去年同期的， 例如  20180630 和 20170630 的数据相比.
def cal_report(report_date_type, report_type, num_of_report, tb="N"):
    cur_year = time.localtime(time.time()).tm_year
    cur_mon = time.localtime(time.time()).tm_mon
    value_tups = []

    i = 1
    while (i <= num_of_report):
        if report_date_type == "year":
            report_date = str(cur_year - i) + "1231"
        elif report_date_type == "season":
            if i == 1:
                report_date = report_utils.get_latest_season_date(cur_year, cur_mon);
            else:
                report_date = report_utils.get_last_season_date(report_date)
        if report_type.startswith("现金"):
            header_tup = ("报告日期", "货币资金(万元)", "准现金类资产(万元)", "总资产(万元)", "净资产(万元)", "货币资金/总资产", "货币资金/净资产")
            header_format_str = "{0[0]:>10}{0[1]:>15}{0[2]:>15}{0[3]:>15}{0[4]:>15}{0[5]:>15}{0[6]:>15}";
            value_format_str = "{0[0]:>13}{0[1]:>19}{0[2]:>21}{0[3]:>18}{0[4]:>19}{0[5]:>20}{0[6]:>20}";
            report_tup = get_tup_zc_xj(report_date)
        elif report_type.startswith("负债"):
            header_tup = (
                "报告日期", "总负债(万元)", "长期借款(万元)", "短期借款(万元)", "应付债券(万元)", "有息负债(万元)", "有息负债/总资产", "一年内到期的非流动负债(万元)",
                "负债总和", "长期递延收益负债(万元)", "资产负债率")
            header_format_str = "{0[0]:>10}{0[1]:>15}{0[2]:>15}{0[3]:>15}{0[4]:>15}{0[5]:>15}{0[6]:>15}{0[7]:>20}{0[8]:>10}{0[9]:>15}{0[10]:>15}";
            value_format_str = "{0[0]:>13}{0[1]:>18}{0[2]:>19}{0[3]:>20}{0[4]:>19}{0[5]:>20}{0[6]:>20}{0[7]:>28}{0[8]:>14}{0[9]:>22}{0[10]:>18}";
            report_tup = get_tup_fz(report_date)
        elif report_type.startswith("固定资产、存货"):
            header_tup = ("报告日期", "固定资产(万元)", "固定资产/总资产", "存货(万元)", "存货/总资产")
            header_format_str = "{0[0]:>10}{0[1]:>15}{0[2]:>15}{0[3]:>15}{0[4]:>15}";
            value_format_str = "{0[0]:>13}{0[1]:>19}{0[2]:>20}{0[3]:>18}{0[4]:>19}";
            report_tup = get_tup_gdzc(report_date)
        elif report_type.startswith("商誉"):
            header_tup = ("报告日期", "商誉(万元)")
            header_format_str = "{0[0]:>10}{0[1]:>15}";
            value_format_str = "{0[0]:>13}{0[1]:>17}";
            report_tup = get_tup_sy(report_date)
        elif report_type.startswith("盈利能力"):
            if tb == "N":
                header_tup = ("报告日期", "营业总收入(万元)", "营业利润(万元)", "利润总额(万元)", "净利润(万元)",
                              "应收票据+应收账款(万元)", "(应收票据+应收账款)/营业总收入", "经营活动产生的现金流量净额(万元)",
                              "经营活动产生的现金流量净额/净利润", "销售商品、提供劳务收到的现金(万元)", "销售商品、提供劳务收到的现金(万元)/营业收入")
                header_format_str = "{0[0]:>10}{0[1]:>15}{0[2]:>15}{0[3]:>15}{0[4]:>15}{0[5]:>15}{0[6]:>20}{0[7]:>20}{0[8]:>20}{0[9]:>20}{0[10]:>25}";
                value_format_str = "{0[0]:>13}{0[1]:>20}{0[2]:>19}{0[3]:>19}{0[4]:>19}{0[5]:>22}{0[6]:>29}{0[7]:>31}{0[8]:>31}{0[9]:>31}{0[10]:>40}";
                report_tup = get_tup_ylnl(report_date)
            else:
                header_tup = ("报告日期", "营业总收入同比", "净利润同比")
                header_format_str = "{0[0]:>10}{0[1]:>15}{0[2]:>15}"
                value_format_str = "{0[0]:>13}{0[1]:>20}{0[2]:>18}"
                report_tup = get_tup_ylnl(report_date, tb)
        if report_tup == None:
            logging.error("没有该财报: %s", report_date)
            i += 1;
            continue;
        value_tups.append(report_tup)
        i += 1
    return get_format_str(report_type, header_tup, value_tups, header_format_str, value_format_str);


def get_format_str(report_type, header_tup, value_tups, header_format_str, value_format_str):
    return "\n" + report_type + common_util.format_table(header_tup, value_tups, header_format_str, value_format_str)


def get_tup_zc_xj(report_date):
    try:
        hbzj, zxjlzc, zzc, jzc, gdzc, ch, sy, yspj, yszk = get_zc(report_date);
    except KeyError as e:
        return None
    hbzj_zzc = None
    if (isinstance(hbzj, (int)) and isinstance(zzc, (int))):
        hbzj_zzc = common_util.cal_percent(hbzj, zzc);
    if (isinstance(hbzj, (int)) and isinstance(jzc, (int))):
        hbzj_jzc = common_util.cal_percent(hbzj, jzc);
    return (report_date, hbzj, zxjlzc, zzc, jzc, hbzj_zzc, hbzj_jzc)


def get_tup_fz(report_date):
    try:
        hbzj, zxjlzc, zzc, jzc, gdzc, ch, sy, yspj, yszk = get_zc(report_date)
    except KeyError as e:
        return None
    zfz, cqjk, dqjk, yfzq, yxfz, cqdysyfz, ynndqfldfz, fzzh = get_fz(report_date)
    yxfz_zzc = common_util.cal_percent(yxfz, zzc) if isinstance(yxfz, (int)) and yxfz != 0 else "--"
    zfz_zzc = common_util.cal_percent(zfz, zzc)
    return (report_date, zfz, cqjk, dqjk, yfzq, yxfz, yxfz_zzc, ynndqfldfz, fzzh, cqdysyfz, zfz_zzc);


def get_tup_gdzc(report_date):
    try:
        hbzj, zxjlzc, zzc, jzc, gdzc, ch, sy, yspj, yszk = get_zc(report_date)
    except KeyError as e:
        return None;
    gdzc_zzc = common_util.cal_percent(gdzc, zzc) if (isinstance(gdzc, (int)) and gdzc != 0) else '--'
    ch_zzc = common_util.cal_percent(ch, zzc) if (isinstance(ch, (int)) and ch != 0) else '--'
    return (report_date, gdzc, gdzc_zzc, ch, ch_zzc);


def get_tup_sy(report_date):
    try:
        hbzj, zxjlzc, zzc, jzc, gdzc, ch, sy, yspj, yszk = get_zc(report_date)
    except KeyError as e:
        return None;
    return (report_date, sy);


def get_tup_ylnl(report_date, tb="N"):
    try:
        hbzj, zxjlzc, zzc, jzc, gdzc, ch, sy, yspj, yszk = get_zc(report_date)
    except KeyError as e:
        return None
    yyzsr, yylr, lrze, jlr = get_lr(report_date)
    jyhdxjllje, xssptglwxj = get_xjll(report_date)

    # (应收票据 + 应收账款)/营业收入
    yspj_yszk = (yspj if isinstance(yspj, (int)) else 0) + (yszk if isinstance(yszk, (int)) else 0)
    yspj_yszk_yysr = common_util.cal_percent(yspj_yszk, yyzsr) if (isinstance(yspj_yszk,
                                                                              (int)) and yspj_yszk != 0) else '--'

    # 经营活动产生的现金流量净额/净利润
    jyhdxjllje_jlr = common_util.cal_percent(jyhdxjllje, jlr) if isinstance(jyhdxjllje,
                                                                            (int)) and jyhdxjllje != 0 else '--'
    # 销售商品、提供劳务收到的现金/营业收入
    xssptglwxj_yysr = common_util.cal_percent(xssptglwxj, yyzsr) if isinstance(xssptglwxj,
                                                                               (int)) and xssptglwxj != 0 else '--'

    if tb == "N":
        return (report_date, yyzsr, yylr, lrze, jlr, yspj_yszk, yspj_yszk_yysr, jyhdxjllje, jyhdxjllje_jlr, xssptglwxj,
                xssptglwxj_yysr);
    else:
        last_year_report_date = report_utils.get_last_year_report_date(report_date)
        (report_date_last, yyzsr_last, yylr_last, lrze_last, jlr_last, yspj_yszk_last, yspj_yszk_yysr_last,
         jyhdxjllje_last, jyhdxjllje_jlr_last, xssptglwxj_last,
         xssptglwxj_yysr_last) = get_tup_ylnl(last_year_report_date, "N")
        yyzsrtb = common_util.cal_percent(yyzsr, yyzsr_last, increase="Y")
        jlrtb = common_util.cal_percent(jlr, jlr_last, increase="Y")
        result_tb = (report_date, yyzsrtb, jlrtb)
        return result_tb;


######################################################## 获取数据 ##################################################################################################

# 获取资产相关数据
def get_zc(report_date):
    hbzj_str = zcfzb_dict['资产']['流动资产']['货币资金(万元)'][report_date]
    zzc_str = zcfzb_dict['资产']["非流动资产"]["资产总计(万元)"][report_date]
    # 净资产 = 股东权益 = 资产总计 - 负债总计
    jzc_str = zcfzb_dict["股东权益"]["所有者权益(或股东权益)合计(万元)"][report_date];
    gdzc_str = zcfzb_dict["资产"]["非流动资产"]["固定资产(万元)"][report_date];
    ch_str = zcfzb_dict["资产"]["流动资产"]["存货(万元)"][report_date]
    sy_str = zcfzb_dict["资产"]["非流动资产"]["商誉(万元)"][report_date]
    yspj_str = zcfzb_dict["资产"]["流动资产"]["应收票据(万元)"][report_date]
    yszk_str = zcfzb_dict["资产"]["流动资产"]["应收账款(万元)"][report_date]
    hbzj, zzc, jzc, gdzc, ch, sy, yspj, yszk = report_utils.trans_money(hbzj_str, zzc_str, jzc_str, gdzc_str, ch_str,
                                                                        sy_str,
                                                                        yspj_str, yszk_str)
    # 准现金类资产 = 货币现金 + 交易性金融资产 + 可供出售金融资产
    jyxjrzc, kzcsjrzc = report_utils.trans_money(zcfzb_dict["资产"]["流动资产"]["交易性金融资产(万元)"][report_date],
                                                 zcfzb_dict["资产"]["非流动资产"]["可供出售金融资产(万元)"][report_date])
    zxjlzc1 = (hbzj if isinstance(hbzj, (int)) else 0) + (jyxjrzc if isinstance(jyxjrzc, (int)) else 0) + (
        kzcsjrzc if isinstance(kzcsjrzc, (int)) else 0)
    zxjlzc = zxjlzc1 if isinstance(zxjlzc1, (int)) and zxjlzc1 != 0 else '--'
    return hbzj, zxjlzc, zzc, jzc, gdzc, ch, sy, yspj, yszk


# 获取负债相关数据
def get_fz(report_date):
    zfz_str = zcfzb_dict["负债"]["非流动负债"]["负债合计(万元)"][report_date]
    zfz, = report_utils.trans_money(zfz_str)
    # 有息负债 = 长期借款 + 短期借款 + 应付债券
    cqjk, dqjk, yfzq, cqdysyfz, ynndqfldfz = report_utils.trans_money(
        zcfzb_dict["负债"]["非流动负债"]["长期借款(万元)"][report_date],
        zcfzb_dict["负债"]["流动负债"]["短期借款(万元)"][report_date],
        zcfzb_dict["负债"]["非流动负债"]["应付债券(万元)"][report_date],
        zcfzb_dict["负债"]["非流动负债"]["长期递延收益(万元)"][report_date],
        zcfzb_dict["负债"]["流动负债"]["一年内到期的非流动负债(万元)"][report_date])
    yxfz1 = (cqjk if isinstance(cqjk, (int)) else 0) + (dqjk if isinstance(dqjk, (int)) else 0) + (
        yfzq if isinstance(yfzq, (int)) else 0)
    yxfz = yxfz1 if isinstance(yxfz1, (int)) and yxfz1 != 0 else '--'
    # 负责总和 = 长期借款 + 短期借款 + 应付债券 + 一年内到期的非流动负债,  负债总和是刚性的， 和资产负债表中的负债总计不同，是负债总计的子集
    fzzh = '--'
    if isinstance(yxfz, (int)) and isinstance(ynndqfldfz, (int)):
        fzzh = yxfz + ynndqfldfz
    elif isinstance(yxfz, (int)) and not isinstance(ynndqfldfz, (int)):
        fzzh = yxfz
    elif not isinstance(yxfz, (int)) and isinstance(ynndqfldfz, (int)):
        fzzh = ynndqfldfz
    return zfz, cqjk, dqjk, yfzq, yxfz, cqdysyfz, ynndqfldfz, fzzh


# 获取利润相关数据
def get_lr(report_date):
    yyzsr, yylr, lrze, jlr, = report_utils.trans_money(lrb_dict["营业总收入(万元)"][report_date],
                                                       lrb_dict["营业利润(万元)"][report_date],
                                                       lrb_dict["利润总额(万元)"][report_date],
                                                       lrb_dict["净利润(万元)"][report_date])
    return yyzsr, yylr, lrze, jlr


# 获取现金流量相关数据.
def get_xjll(report_date):
    jyhdxjllje, = report_utils.trans_money(xjllb_dict["一、经营活动产生的现金流量"]["经营活动产生的现金流量净额(万元)"][report_date])
    xssptglwxj, = report_utils.trans_money(xjllb_dict["一、经营活动产生的现金流量"]["销售商品、提供劳务收到的现金(万元)"][report_date])
    return jyhdxjllje, xssptglwxj


def assign_dict(code):
    collection_pre = "financial_"
    # 要修改全局变量，需加global
    global lrb_dict, xjllb_dict, zcfzb_dict
    lrb_dict = report_utils.get_one_record_dict(collection_pre + "lrb", code);
    xjllb_dict = report_utils.get_one_record_dict(collection_pre + "xjllb", code)
    zcfzb_dict = report_utils.get_one_record_dict(collection_pre + "zcfzb", code)
    if (common_util.is_any_none(lrb_dict, xjllb_dict, zcfzb_dict)):
        logging.error("lrb_dict, xjllb_dict, zcfzb_dict 有的为None, 可能 code=%s 不存在", code)
        return False
    return True;


query_one("002308", "season", 10)

this_selected_codes = {"000736": "中交地产", "601318": "中国平安", "000001": "平安银行"}
# query_statistics("20171231", selected_codes=this_selected_codes)
