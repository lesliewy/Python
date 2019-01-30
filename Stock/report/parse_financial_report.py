import json
import time

from download import sombrero
from mystring import string_util

from Stocks import *

###############################################
#
# 从网易财经上获取财报数据.  http://quotes.money.163.com/f10/xjllb_603220.html
# 包括: 资产负债表、利润表、现金流量表.
# 当天可重复执行, 重复执行后只处理第一次没下载完的文件。
#
###############################################


# 日志
LOG_FORMAT = "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename='log/parse.log', level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)

local_dir = "data/financial_report/";
url_lrb_t = "http://quotes.money.163.com/f10/lrb_{code}.html";
url_zcfzb_t = "http://quotes.money.163.com/f10/zcfzb_{code}.html";
url_xjllb_t = "http://quotes.money.163.com/f10/xjllb_{code}.html"

selector_lrb_column_key = "#scrollTable > div.col_r > table > tbody > tr";
selector_lrb_line_key = "#scrollTable > div.col_l > table > tbody > tr";
selector_lrb_value = "#scrollTable > div.col_r > table > tbody > tr";

selector_zcfzb_column_key = "#scrollTable > div.col_r > table > tbody > tr";
selector_zcfzb_line_key = "#scrollTable > div.col_l > table > tbody > tr";
selector_zcfzb_value = "#scrollTable > div.col_r > table > tbody > tr";

selector_xjllb_column_key = "#scrollTable > div.col_r > table > tbody > tr";
selector_xjllb_line_key = "#scrollTable > div.col_l > table > tbody > tr"
selector_xjllb_value = "#scrollTable > div.col_r > table > tbody > tr";

arch_template_zcfzb = {"资产": {
    "流动资产": ["货币资金(万元)", "结算备付金(万元)", "拆出资金(万元)", "交易性金融资产(万元)", "衍生金融资产(万元)", "应收票据(万元)", "应收账款(万元)", "预付款项(万元)",
             "应收保费(万元)", "应收分保账款(万元)", "应收分保合同准备金(万元)", "应收利息(万元)", "应收股利(万元)", "其他应收款(万元)", "应收出口退税(万元)", "应收补贴款(万元)",
             "应收保证金(万元)", "内部应收款(万元)", "买入返售金融资产(万元)", "存货(万元)", "待摊费用(万元)", "待处理流动资产损益(万元)", "一年内到期的非流动资产(万元)",
             "其他流动资产(万元)", "流动资产合计(万元)"],
    "非流动资产": ["发放贷款及垫款(万元)", "可供出售金融资产(万元)", "持有至到期投资(万元)", "长期应收款(万元)", "长期股权投资(万元)", "其他长期投资(万元)", "投资性房地产(万元)",
              "固定资产原值(万元)", "累计折旧(万元)", "固定资产净值(万元)", "固定资产减值准备(万元)", "固定资产(万元)", "在建工程(万元)", "工程物资(万元)", "固定资产清理(万元)",
              "生产性生物资产(万元)", "公益性生物资产(万元)", "油气资产(万元)", "无形资产(万元)", "开发支出(万元)", "商誉(万元)", "长期待摊费用(万元)", "股权分置流通权(万元)",
              "递延所得税资产(万元)", "其他非流动资产(万元)", "非流动资产合计(万元)", "资产总计(万元)"]}, "负债": {
    "流动负债": ["短期借款(万元)", "向中央银行借款(万元)", "吸收存款及同业存放(万元)", "拆入资金(万元)", "交易性金融负债(万元)", "衍生金融负债(万元)", "应付票据(万元)",
             "应付账款(万元)", "预收账款(万元)", "卖出回购金融资产款(万元)", "应付手续费及佣金(万元)", "应付职工薪酬(万元)", "应交税费(万元)", "应付利息(万元)", "应付股利(万元)",
             "其他应交款(万元)", "应付保证金(万元)", "内部应付款(万元)", "其他应付款(万元)", "预提费用(万元)", "预计流动负债(万元)", "应付分保账款(万元)", "保险合同准备金(万元)",
             "代理买卖证券款(万元)", "代理承销证券款(万元)", "国际票证结算(万元)", "国内票证结算(万元)", "递延收益(万元)", "应付短期债券(万元)", "一年内到期的非流动负债(万元)",
             "其他流动负债(万元)", "流动负债合计(万元)"],
    "非流动负债": ["长期借款(万元)", "应付债券(万元)", "长期应付款(万元)", "专项应付款(万元)", "预计非流动负债(万元)", "长期递延收益(万元)", "递延所得税负债(万元)",
              "其他非流动负债(万元)", "非流动负债合计(万元)", "负债合计(万元)"]},
    "股东权益": ["实收资本(或股本)(万元)", "资本公积(万元)", "减:库存股(万元)", "专项储备(万元)", "盈余公积(万元)", "一般风险准备(万元)",
             "未确定的投资损失(万元)", "未分配利润(万元)", "拟分配现金股利(万元)", "外币报表折算差额(万元)", "归属于母公司股东权益合计(万元)",
             "少数股东权益(万元)", "所有者权益(或股东权益)合计(万元)", "负债和所有者权益(或股东权益)总计(万元)"]};

arch_template_xjllb = {
    "一、经营活动产生的现金流量": ["销售商品、提供劳务收到的现金(万元)", "客户存款和同业存放款项净增加额(万元)", "向中央银行借款净增加额(万元)", "向其他金融机构拆入资金净增加额(万元)",
                      "收到原保险合同保费取得的现金(万元)", "收到再保险业务现金净额(万元)", "保户储金及投资款净增加额(万元)", "处置交易性金融资产净增加额(万元)",
                      "收取利息、手续费及佣金的现金(万元)", "拆入资金净增加额(万元)", "回购业务资金净增加额(万元)", "收到的税费返还(万元)", "收到的其他与经营活动有关的现金(万元)",
                      "经营活动现金流入小计(万元)", "购买商品、接受劳务支付的现金(万元)", "客户贷款及垫款净增加额(万元)", "存放中央银行和同业款项净增加额(万元)",
                      "支付原保险合同赔付款项的现金(万元)", "支付利息、手续费及佣金的现金(万元)", "支付保单红利的现金(万元)", "支付给职工以及为职工支付的现金(万元)", "支付的各项税费(万元)",
                      "支付的其他与经营活动有关的现金(万元)", "经营活动现金流出小计(万元)", "经营活动产生的现金流量净额(万元)"],
    "二、投资活动产生的现金流量": ["收回投资所收到的现金(万元)", "取得投资收益所收到的现金(万元)", "处置固定资产、无形资产和其他长期资产所收回的现金净额(万元)", "处置子公司及其他营业单位收到的现金净额(万元)",
                      "收到的其他与投资活动有关的现金(万元)", "减少质押和定期存款所收到的现金(万元)", "投资活动现金流入小计(万元)", "购建固定资产、无形资产和其他长期资产所支付的现金(万元)",
                      "投资所支付的现金(万元)", "质押贷款净增加额(万元)", "取得子公司及其他营业单位支付的现金净额(万元)", "支付的其他与投资活动有关的现金(万元)",
                      "增加质押和定期存款所支付的现金(万元)", "投资活动现金流出小计(万元)", "投资活动产生的现金流量净额(万元)"],
    "三、筹资活动产生的现金流量": ["吸收投资收到的现金(万元)", "其中：子公司吸收少数股东投资收到的现金(万元)", "取得借款收到的现金(万元)", "发行债券收到的现金(万元)",
                      "收到其他与筹资活动有关的现金(万元)", "筹资活动现金流入小计(万元)", "偿还债务支付的现金(万元)", "分配股利、利润或偿付利息所支付的现金(万元)",
                      "其中：子公司支付给少数股东的股利、利润(万元)", "支付其他与筹资活动有关的现金(万元)", "筹资活动现金流出小计(万元)", "筹资活动产生的现金流量净额(万元)"],
    "四、汇率变动对现金及现金等价物的影响": ["汇率变动对现金及现金等价物的影响(万元)"],
    "五、现金及现金等价物净增加额": ["现金及现金等价物净增加额(万元)", "加:期初现金及现金等价物余额(万元)", "期末现金及现金等价物余额(万元)"], "补充资料": {
        "1、将净利润调节为经营活动的现金流量": ["净利润(万元)", "少数股东损益(万元)", "未确认的投资损失(万元)", "资产减值准备(万元)", "固定资产折旧、油气资产折耗、生产性物资折旧(万元)",
                               "无形资产摊销(万元)", "长期待摊费用摊销(万元)", "待摊费用的减少(万元)", "预提费用的增加(万元)", "处置固定资产、无形资产和其他长期资产的损失(万元)",
                               "固定资产报废损失(万元)", "公允价值变动损失(万元)", "递延收益增加(减：减少)(万元)", "预计负债(万元)", "财务费用(万元)", "投资损失(万元)",
                               "递延所得税资产减少(万元)", "递延所得税负债增加(万元)", "存货的减少(万元)", "经营性应收项目的减少(万元)", "经营性应付项目的增加(万元)",
                               "已完工尚未结算款的减少(减:增加)(万元)", "已结算尚未完工款的增加(减:减少)(万元)", "其他(万元)", "经营活动产生现金流量净额(万元)"],
        "2、不涉及现金收支的重大投资和筹资活动": ["债务转为资本(万元)", "一年内到期的可转换公司债券(万元)", "融资租入固定资产(万元)"],
        "3、现金及现金等价物净变动": ["现金的期末余额(万元)", "现金的期初余额(万元)", "现金等价物的期末余额(万元)", "现金等价物的期初余额(万元)", "现金及现金等价物的净增加额(万元)"]}};


def main():
    logging.info("==================== 开始获取财务报表...")
    start = time.time()
    codes = Stocks.get_codes();
    if (not codes):
        logging.error("没有取到code.");
        return;
    i = 0;
    for code in codes:
        if (i > 2):
            break;
        get_three_report(code);
        i += 1;
    end = time.time();
    logging.info("==================== 获取财务报表完成: %f s", (end - start))


def get_three_report(code):
    get_lrb(code);
    get_zcfzb(code)
    get_xjllb(code);


def get_lrb(code):
    logging.info("正在获取利润表数据. code = %s", code);
    if (string_util.is_any_blank(code)):
        logging.error("code 不能为空");
        return;
    type = "lrb";
    url_lrb = url_lrb_t.replace("{code}", code);
    html_full_path, json_full_path = __get_file_path(code, type);
    if (os.path.isfile(json_full_path)):
        logging.info("%s 已被处理.", code)
        return;

    f, soup = sombrero.get_soup(url_lrb, html_full_path, file_size=2000);
    if (not soup):
        logging.error("soup 获取失败.");
        return;

    colume_key_dict = sombrero.get_key(soup, selector_lrb_column_key, key_location="H", key_seq=0);
    line_key_dict = sombrero.get_key(soup, selector_lrb_line_key, key_location="V", key_seq=0);

    result = sombrero.get_value(soup, selector_lrb_value, exclude_top=True, colume_key_dict=colume_key_dict,
                                exclude_left=False, line_key_dict=line_key_dict)

    result_file = open(json_full_path, "w", encoding='utf-8')
    json.dump(result, result_file, ensure_ascii=False, indent=4)

    if (f):
        f.close();


def get_zcfzb(code):
    logging.info("正在获取资产负债表数据. code = %s", code);
    if (string_util.is_any_blank(code)):
        logging.error("code 不能为空");
        return;
    type = "zcfzb";
    url_zcfzb = url_zcfzb_t.replace("{code}", code);
    html_full_path, json_full_path = __get_file_path(code, type);
    if (os.path.isfile(json_full_path)):
        logging.info("%s 已被处理.", code)
        return;

    f, soup = sombrero.get_soup(url_zcfzb, html_full_path, file_size=2000);
    if (not soup):
        logging.error("soup 获取失败.");
        return;

    colume_key_dict = sombrero.get_key(soup, selector_zcfzb_column_key, key_location="H", key_seq=0);
    line_key_dict = sombrero.get_key(soup, selector_lrb_line_key, key_location="V", key_seq=0);

    result_original = sombrero.get_value(soup, selector_lrb_value, exclude_top=True, colume_key_dict=colume_key_dict,
                                         exclude_left=False, line_key_dict=line_key_dict)
    result = sombrero.adjust_architecture_dict(arch_template_zcfzb, result_original);
    result_file = open(json_full_path, "w", encoding='utf-8')
    json.dump(result, result_file, ensure_ascii=False, indent=4)

    if (f):
        f.close();


def get_xjllb(code):
    logging.info("正在获取现金流量表数据. code = %s", code);
    if (string_util.is_any_blank(code)):
        logging.error("code 不能为空");
        return;
    type = "xjllb";
    url_xjllb = url_xjllb_t.replace("{code}", code);
    html_full_path, json_full_path = __get_file_path(code, type);
    if (os.path.isfile(json_full_path)):
        logging.info("%s 已被处理.", code)
        return;

    f, soup = sombrero.get_soup(url_xjllb, html_full_path, file_size=2000);
    if (not soup):
        logging.error("soup 获取失败.");
        return;

    colume_key_dict = sombrero.get_key(soup, selector_xjllb_column_key, key_location="H", key_seq=0);
    line_key_dict = sombrero.get_key(soup, selector_xjllb_line_key, key_location="V", key_seq=0);

    result_original = sombrero.get_value(soup, selector_xjllb_value, exclude_top=True, colume_key_dict=colume_key_dict,
                                         exclude_left=False, line_key_dict=line_key_dict)
    result = sombrero.adjust_architecture_dict(arch_template_xjllb, result_original);
    result_file = open(json_full_path, "w", encoding='utf-8')
    json.dump(result, result_file, ensure_ascii=False, indent=4)

    if (f):
        f.close();


def __get_file_path(code, type):
    dir_date = time.strftime('%Y/%m/%d/', time.localtime());
    full_dir = os.path.join(local_dir, dir_date, type);
    if (not os.path.isdir(full_dir)):
        os.makedirs(full_dir);
    html_full_path = os.path.join(full_dir, type + "_" + code + ".html")
    json_full_path = html_full_path.replace(".html", ".json");
    return html_full_path, json_full_path


main()
