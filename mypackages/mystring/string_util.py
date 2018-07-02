# coding:utf-8

import numbers

# 从str中取出数字.
def get_num(value):
    if len(value) <= 0:
        return

    result = ""
    for j in value:
        if (j >= '0' and j <= '9') or j == '.':
            result += j
    return result

def a():
    html = "a/b/c.html"
    print(html.replace("\.html", "\.dat"))

