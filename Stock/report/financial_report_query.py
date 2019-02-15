import logging

from db import mongo
from mystring import string_util
from myutils import common_util

# 日志
LOG_FORMAT = "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename='../log/query.log', level=logging.INFO, format=LOG_FORMAT,
                    datefmt=DATE_FORMAT)

# mongodb 连接
dbname = "stock";
collection_pre = "financial_"
username = "stock"
password = "stock123"
db = mongo.get_mongo_db(dbname, username, password);

# 一条记录
lrb_dict, xjllb_dict, zcfzb_dict = None, None, None


def main(code, report_date):
    logging.info("code=%s", code)
    if (string_util.is_any_blank(code)):
        logging.error("code 不能为空.")
        return;
    if (not assign_dict(code)):
        return;
    cal_zc_xj(report_date)
    cal_fz_xj(report_date)
    cal_gdzc(report_date)
    cal_sy(report_date)
    cal_ylnl(report_date)


# 现金情况
def cal_zc_xj(report_date):
    hbzj, zxjlzc, zzc, jzc, gdzc, ch, sy, yspj, yszk = get_zc(report_date);
    hbzj_zzc = None
    if (isinstance(hbzj, (int)) and isinstance(zzc, (int))):
        hbzj_zzc = common_util.cal_percent(hbzj, zzc);
    if (isinstance(hbzj, (int)) and isinstance(jzc, (int))):
        hbzj_jzc = common_util.cal_percent(hbzj, jzc);
    # logging.info("报告日期: %s, 货币资金(万元): %s, 准现金类资产(万元): %s, 总资产(万元): %s, 净资产(万元): %s, 货币资金/总资产: %s, 货币资金/净资产: %s",
    #              report_date,
    #              hbzj, zxjlzc, zzc,
    #              jzc, hbzj_zzc, hbzj_jzc);
    header_format_str = "{0[0]:>10}{0[1]:>15}{0[2]:>15}{0[3]:>15}{0[4]:>15}{0[5]:>15}{0[6]:>15}";
    value_format_str = "{0[0]:>13}{0[1]:>19}{0[2]:>21}{0[3]:>18}{0[4]:>19}{0[5]:>20}{0[6]:>20}";
    logging.info("\n现金情况:" +
                 common_util.format_table(
                     ("报告日期", "货币资金(万元)", "准现金类资产(万元)", "总资产(万元)", "净资产(万元)", "货币资金/总资产", "货币资金/净资产"),
                     [(report_date, hbzj, zxjlzc, zzc, jzc, hbzj_zzc, hbzj_jzc)], header_format_str,
                     value_format_str))
    return;


# 负债情况
def cal_fz_xj(report_date):
    hbzj, zxjlzc, zzc, jzc, gdzc, ch, sy, yspj, yszk = get_zc(report_date)
    zfz, cqjk, dqjk, yfzq, yxfz, cqdysyfz = get_fz(report_date)
    yxfz_zzc = common_util.cal_percent(yxfz, zzc) if isinstance(yxfz, (int)) and yxfz > 0 else "--"
    zfz_zzc = common_util.cal_percent(zfz, zzc)
    # logging.info(
    #     "报告日期: %s, 总负债(万元): %s, 长期借款(万元): %s, 短期借款(万元): %s, 应付债券(万元): %s, 有息负债(万元): %s, 有息负债/总资产: %s, 长期递延收益负债(万元): %s, 资产负债率: %s",
    #     report_date, zfz,
    #     cqjk, dqjk, yfzq, yxfz, yxfz_zzc, cqdysyfz, zfz_zzc);
    header_format_str = "{0[0]:>10}{0[1]:>15}{0[2]:>15}{0[3]:>15}{0[4]:>15}{0[5]:>15}{0[6]:>15}{0[7]:>15}{0[8]:>15}";
    value_format_str = "{0[0]:>13}{0[1]:>18}{0[2]:>19}{0[3]:>20}{0[4]:>19}{0[5]:>20}{0[6]:>20}{0[7]:>22}{0[8]:>18}";
    logging.info("\n负债情况:" + common_util.format_table(
        ("报告日期", "总负债(万元)", "长期借款(万元)", "短期借款(万元)", "应付债券(万元)", "有息负债(万元)", "有息负债/总资产", "长期递延收益负债(万元)", "资产负债率"),
        [(report_date, zfz, cqjk, dqjk, yfzq, yxfz, yxfz_zzc, cqdysyfz, zfz_zzc)], header_format_str, value_format_str))
    return;


# 存货, 固定资产, 固定资产/总资产, 固定资产构成没法获取，不然可以查看其中房地产占比.
def cal_gdzc(report_date):
    hbzj, zxjlzc, zzc, jzc, gdzc, ch, sy, yspj, yszk = get_zc(report_date)
    gdzc_zzc = common_util.cal_percent(gdzc, zzc) if (isinstance(gdzc, (int)) and gdzc > 0) else '--'
    ch_zzc = common_util.cal_percent(ch, zzc) if (isinstance(ch, (int)) and ch > 0) else '--'
    # logging.info("报告日期: %s, 固定资产(万元): %s, 固定资产/总资产: %s, 存货(万元): %s, 存货/总资产: %s", report_date, gdzc, gdzc_zzc, ch,
    #              ch_zzc);
    header_format_str = "{0[0]:>10}{0[1]:>15}{0[2]:>15}{0[3]:>15}{0[4]:>15}";
    value_format_str = "{0[0]:>13}{0[1]:>19}{0[2]:>20}{0[3]:>18}{0[4]:>19}";
    logging.info("\n固定资产、存货:" + common_util.format_table(("报告日期", "固定资产(万元)", "固定资产/总资产", "存货(万元)", "存货/总资产"),
                                                         [(report_date, gdzc, gdzc_zzc, ch, ch_zzc)], header_format_str,
                                                         value_format_str))
    return;


# 商誉
def cal_sy(report_date):
    hbzj, zxjlzc, zzc, jzc, gdzc, ch, sy, yspj, yszk = get_zc(report_date)
    # logging.info("报告日期: %s, 商誉(万元): %s", report_date, sy)
    header_format_str = "{0[0]:>10}{0[1]:>15}";
    value_format_str = "{0[0]:>13}{0[1]:>17}";
    logging.info("\n商誉:" + common_util.format_table(("报告日期", "商誉(万元)"), [(report_date, sy)], header_format_str,
                                                    value_format_str))
    return;


# 盈利能力: 营业收入(可惜没法获取其构成,看看主营收入占比)销售净利率(%)    营运能力: 总资产周转率(次)
def cal_ylnl(report_date):
    hbzj, zxjlzc, zzc, jzc, gdzc, ch, sy, yspj, yszk = get_zc(report_date)
    yyzsr, yylr, lrze, jlr = get_lr(report_date)
    jyhdxjllje, = get_xjll(report_date)

    # 经营活动产生的现金流量净额/净利润
    jyhdxjllje_jlr = common_util.cal_percent(jyhdxjllje, jlr) if isinstance(jyhdxjllje,
                                                                            (int)) and jyhdxjllje > 0 else '--'

    # (应收票据 + 应收账款)/营业收入
    yspj_yszk = (yspj if isinstance(yspj, (int)) else 0) + (yszk if isinstance(yszk, (int)) else 0)
    yspj_yszk_yysr = common_util.cal_percent(yspj_yszk, yyzsr) if (isinstance(yspj_yszk,
                                                                              (int)) and yspj_yszk > 0) else '--'

    # logging.info(
    #     "报告日期: %s, 营业总收入(万元): %s, 营业利润(万元): %s, 利润总额(万元): %s, 净利润(万元): %s, 应收票据+应收账款(万元): %s, (应收票据+应收账款)/营业总收入: %s, 经营活动产生的现金流量净额(万元): %s, 经营活动产生的现金流量净额/净利润: %s",
    #     report_date, yyzsr, yylr, lrze,
    #     jlr, yspj_yszk, yspj_yszk_yysr, jyhdxjllje, jyhdxjllje_jlr)
    header_format_str = "{0[0]:>10}{0[1]:>15}{0[2]:>15}{0[3]:>15}{0[4]:>15}{0[5]:>15}{0[6]:>20}{0[7]:>20}{0[8]:>20}";
    value_format_str = "{0[0]:>13}{0[1]:>20}{0[2]:>19}{0[3]:>19}{0[4]:>19}{0[5]:>22}{0[6]:>29}{0[7]:>31}{0[8]:>31}";
    logging.info("\n盈利能力:" + common_util.format_table(("报告日期", "营业总收入(万元)", "营业利润(万元)", "利润总额(万元)", "净利润(万元)",
                                                       "应收票据+应收账款(万元)", "(应收票据+应收账款)/营业总收入", "经营活动产生的现金流量净额(万元)",
                                                       "经营活动产生的现金流量净额/净利润"), [(report_date, yyzsr, yylr, lrze, jlr,
                                                                               yspj_yszk, yspj_yszk_yysr, jyhdxjllje,
                                                                               jyhdxjllje_jlr)], header_format_str,
                                                      value_format_str))
    return;


#########################################################################################################

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
    hbzj, zzc, jzc, gdzc, ch, sy, yspj, yszk = trans_money(hbzj_str, zzc_str, jzc_str, gdzc_str, ch_str, sy_str,
                                                           yspj_str, yszk_str)
    # 准现金类资产 = 货币现金 + 交易性金融资产 + 可供出售金融资产
    jyxjrzc, kzcsjrzc = trans_money(zcfzb_dict["资产"]["流动资产"]["交易性金融资产(万元)"][report_date],
                                    zcfzb_dict["资产"]["非流动资产"]["可供出售金融资产(万元)"][report_date])
    zxjlzc1 = (hbzj if isinstance(hbzj, (int)) else 0) + (jyxjrzc if isinstance(jyxjrzc, (int)) else 0) + (
        kzcsjrzc if isinstance(kzcsjrzc, (int)) else 0)
    zxjlzc = zxjlzc1 if isinstance(zxjlzc1, (int)) and zxjlzc1 > 0 else '--'
    return hbzj, zxjlzc, zzc, jzc, gdzc, ch, sy, yspj, yszk


# 获取负债相关数据
def get_fz(report_date):
    zfz_str = zcfzb_dict["负债"]["非流动负债"]["负债合计(万元)"][report_date]
    zfz, = trans_money(zfz_str)
    # 有息负债 = 长期借款 + 短期借款 + 应付债券
    cqjk, dqjk, yfzq, cqdysyfz = trans_money(zcfzb_dict["负债"]["非流动负债"]["长期借款(万元)"][report_date],
                                             zcfzb_dict["负债"]["流动负债"]["短期借款(万元)"][report_date],
                                             zcfzb_dict["负债"]["非流动负债"]["应付债券(万元)"][report_date],
                                             zcfzb_dict["负债"]["非流动负债"]["长期递延收益(万元)"][report_date])
    yxfz1 = (cqjk if isinstance(cqjk, (int)) else 0) + (dqjk if isinstance(dqjk, (int)) else 0) + (
        yfzq if isinstance(yfzq, (int)) else 0)
    yxfz = yxfz1 if isinstance(yxfz1, (int)) and yxfz1 > 0 else '--'
    return zfz, cqjk, dqjk, yfzq, yxfz, cqdysyfz


# 获取利润相关数据
def get_lr(report_date):
    yyzsr, yylr, lrze, jlr, = trans_money(lrb_dict["营业总收入(万元)"][report_date], lrb_dict["营业利润(万元)"][report_date],
                                          lrb_dict["利润总额(万元)"][report_date], lrb_dict["净利润(万元)"][report_date])
    return yyzsr, yylr, lrze, jlr


# 获取现金流量相关数据.
def get_xjll(report_date):
    jyhdxjllje, = trans_money(xjllb_dict["一、经营活动产生的现金流量"]["经营活动产生的现金流量净额(万元)"][report_date])
    return jyhdxjllje,


def assign_dict(code):
    # 要修改全局变量，需加global
    global lrb_dict, xjllb_dict, zcfzb_dict
    lrb_dict = get_one_record_dict(collection_pre + "lrb", code);
    xjllb_dict = get_one_record_dict(collection_pre + "xjllb", code)
    zcfzb_dict = get_one_record_dict(collection_pre + "zcfzb", code)
    if (common_util.is_any_none(lrb_dict, xjllb_dict, zcfzb_dict)):
        logging.error("lrb_dict, xjllb_dict, zcfzb_dict 有的为None, 可能 code=%s 不存在", code)
        return False
    return True;


def get_one_record_dict(collection_name, code):
    if (string_util.is_any_blank(collection_name, code)):
        logging.error("collection_name, code 不能为空.");
        return;
    record = list(db[collection_name].find({"code": code}))
    return dict(record[0]) if record and len(record) > 0 else None


def trans_money(*strs):
    result = ()
    for s in strs:
        if s.find('-') > -1:
            result += (s,)
        else:
            result += (int(s.replace(',', '')),)
    return result


main("603313", "20171231")
