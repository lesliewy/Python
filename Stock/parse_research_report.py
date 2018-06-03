# -*- coding:utf-8 -*-

import urllib.request
import json
from Stocks import *
from datetime import date
from bs4 import BeautifulSoup

key_words = ['龙头', '领先', '行业第']

# 为了获取股票所属行业
industry_url = 'http://data.eastmoney.com/report/$$.html'

research_report_url = 'http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&ps=50&p=1&code=$$&rt=50652254'

# 按行业分类结果
research_industry_result_file = 'research_industry_report.data'
# 按概念分类结果
research_notion_result_file = 'research_notion_report.data'

# 概念、code映射文件.
notion_code_file = 'notion_code.data'


# 解析概念板块
def parse_notion_code(notion_code_file):
    result = {}
    file_handle = open(notion_code_file, 'r')
    for line in file_handle:
        notion_name = line.split(',')[0].strip()
        code = line.split(',')[1].strip()
        if (code in result):
            result[code].add(notion_name)
        else:
            s = set()
            s.add(notion_name)
            result[code] = s
    return result


# 获取需要的文件
def get_research_files(code):
    today = date.today().isoformat()
    json_file = today + '/' + code + '.data'
    html_file = today + '/' + code + '.html'
    # 本地存在文件，则读取本地的.
    if (os.path.isfile(json_file) and os.path.isfile(html_file)):
        file_handle = open(json_file, 'r')
        return file_handle.read()
    if (not os.path.isdir(today)):
        os.mkdir(today)

    json_url = research_report_url.replace('$$', code)
    persist_file(json_url, json_file, 'utf-8')

    html_url = industry_url.replace('$$', code)
    persist_file(html_url, html_file, 'GBK')

    file_handle = open(json_file, 'r')
    return file_handle.read()


# 获取指定url, 保存至本地
def persist_file(url, file, encoding):
    try:
        # 构建请求的request
        request = urllib.request.Request(url)
        # 利用urlopen获取页面代码
        response = urllib.request.urlopen(request)
        # 将页面转换编码
        content = response.read().decode(encoding)

        # 保存至文件
        file_handle = open(file, 'w')
        file_handle.write(content)
        file_handle.close()
        return content
    except urllib.request.URLError as e:
        if hasattr(e, "reason"):
            print("连接失败,错误原因", e.reason)
            return None


# 获取所有的code
def get_codes():
    codes = Stocks.get_codes()
    logging.info("获取code数: " + str(len(codes)))
    return codes


# 解析研报
def parse_research_report(code):
    research_json = get_research_files(code)
    # 不存在研报时,json: ([{stats:false}])
    if (not research_json or research_json == '([{stats:false}])'):
        logging.info('不存在研报: ' + code)
        return
    # 去掉前后()
    research_json = research_json[1:-1]

    all_reports = json.loads(research_json)
    if (not all_reports):
        logging.info('不存在研报: ' + code)
        return
    calc_dict = {}
    existed = False
    # 初始化
    for key_word in key_words:
        calc_dict[key_word] = 0
    for report in all_reports:
        title = report["title"]
        for key_word in key_words:
            if (title.count(key_word) > 0):
                calc_dict[key_word] = calc_dict[key_word] + 1
                existed = True
    # 没有找到任何一个关键词时，直接退出.
    if (not existed):
        return

    # soup
    today = date.today().isoformat()
    html_file_path = today + '/' + code + '.html'
    if (not os.path.isfile(html_file_path)):
        return
    html_file = open(html_file_path, 'r', encoding='utf-8')
    soup = BeautifulSoup(html_file, 'html5lib')  # html.parser   html5lib  lxml

    # 名称
    stock_name_long = soup.select('#s1-tab > li.at')[0].string
    stock_name = stock_name_long[0:stock_name_long.find('(')]

    # 行业
    industry = soup.select('#s1-tab > li:nth-of-type(2)')[0].string.replace('研报', '')

    # 保存至文件
    today = date.today().isoformat()
    industry_file_path = today + '/' + research_industry_result_file
    industry_file_handle = open(industry_file_path, 'a')
    industry_content = industry + ',' + code + ',' + stock_name + ',' + str(calc_dict) + "\n"
    industry_file_handle.write(industry_content)
    industry_file_handle.close()

    notion_file_path = today + '/' + research_notion_result_file
    notion_file_handle = open(notion_file_path, 'a')
    notion_names = notion_dict.get(code)
    if notion_names:
        for notion_name in notion_names:
            notion_content = notion_name + ',' + code + ',' + stock_name + ',' + str(calc_dict) + "\n"
            notion_file_handle.write(notion_content)
        notion_file_handle.close()


def sort_file(file_path):
    f = open(file_path)
    result = []
    iter_f = iter(f)  # 用迭代器循环访问文件中的每一行
    for line in iter_f:
        result.append(line)
    f.close()
    result.sort()
    f = open(file_path, 'w')
    f.writelines(result)
    f.close()


# 概念板块对应的code
notion_dict = parse_notion_code(notion_code_file)


def main():
    codes = get_codes()
    # codes = ['002707']
    index = 0;
    # 先删掉
    today = date.today().isoformat()
    industry_file_path = today + '/' + research_industry_result_file
    if (os.path.isfile(industry_file_path)):
        os.remove(industry_file_path)
    notion_file_path = today + '/' + research_notion_result_file
    if (os.path.isfile(notion_file_path)):
        os.remove(notion_file_path)
    for code in codes:
        index += 1
        logging.info("正在处理: " + str(index) + " " + code)
        parse_research_report(code)
    # 对文件排序
    today = date.today().isoformat()
    industry_file_path = today + '/' + research_industry_result_file
    sort_file(industry_file_path)
    notion_file_path = today + '/' + research_notion_result_file
    sort_file(notion_file_path)


# get_codes()

# print(getPage())

main()
