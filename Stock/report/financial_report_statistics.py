from ..Stocks import *
from ..report import report_utils


# 资产负债率
def cal_fz_zc(report_date, selected_codes={}, reverse=False):
    if len(selected_codes) > 0:
        codes_dict = selected_codes
    else:
        codes_dict = Stocks.get_code_name_dict_from_file()
    fz_zc_dict = {}
    # index = 1
    for code in codes_dict:
        # if index > 100:
        #     break;
        zcfzb_dict = report_utils.get_one_record_dict("financial_zcfzb", code)
        try:
            zzc, zfz = report_utils.trans_money(zcfzb_dict['资产']["非流动资产"]["资产总计(万元)"][report_date],
                                                zcfzb_dict["负债"]["非流动负债"]["负债合计(万元)"][report_date])
        except Exception:
            continue
        if isinstance(zzc, (int)) and isinstance(zfz, (int)):
            zfz_zzc = zfz / zzc
            fz_zc_dict[code + "(" + codes_dict[code] + ")"] = zfz_zzc
        # index += 1
    fz_zc_dict_sorted = sorted(fz_zc_dict.items(), key=lambda x: x[1], reverse=reverse)
    result = {}
    for tup in fz_zc_dict_sorted:
        key = tup[0]
        original_val = tup[1]
        result[key] = str(round(original_val * 100, 2)) + "%"
    return result
