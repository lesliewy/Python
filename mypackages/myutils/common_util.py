def is_any_none(*values):
    for v in values:
        if v == None:
            return True;
    return False;


# reserved: 小数点位数;   increase: 计算增加的比例, a 相对 b 增加了多少比例, 例如 a=10, b= 5, increase="Y", 结果就是100%.
def cal_percent(a, b, reserved=2, increase="N"):
    if (not isinstance(a, (int)) and not isinstance(a, (float))) and (
            not isinstance(b, (int)) and not isinstance(b, (float))):
        return ""
    if increase == "N":
        return str(round(a / b * 100, reserved)) + "%"
    else:
        return str(round((a - b) / b * 100, reserved)) + "%"


# 如果header、value 一个是中文，一个是英文，如果使用同一个format_str 就会出现不对齐情况;
def format_table(header_tup, value_tups, header_format_str, value_format_str):
    if is_any_none(header_tup, value_tups, header_format_str, value_format_str) or len(header_tup) == 0 or len(
            value_tups) == 0 or len(
        header_format_str.strip()) == 0 or len(value_format_str.strip()) == 0:
        return;
    result = "\n" + header_format_str.format(header_tup) + "\n"
    for value_tup in value_tups:
        result += value_format_str.format(value_tup) + "\n"
    return result


def format_table_dict(val_dict, num_output):
    if val_dict == None:
        return;
    result = ""
    seq = 1
    for key in val_dict:
        if (seq > num_output):
            break;
        result += '{0:>10}{1:>20}{2:>10}\n'.format(seq, key, val_dict[key])
        seq += 1
    return result
