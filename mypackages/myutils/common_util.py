def is_any_none(*values):
    for v in values:
        if v == None:
            return True;
    return False;


def cal_percent(a, b, reserved=2):
    if (not isinstance(a, (int)) and not isinstance(a, (float))) and (
            not isinstance(b, (int)) and not isinstance(b, (float))):
        return ""
    return str(round(a / b * 100, reserved)) + "%"


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
