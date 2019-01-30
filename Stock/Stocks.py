# -*- coding:utf-8 -*-

import os
import logging
import urllib.request

'''
   东方财富 - 数据中心 - 个股资金流 - 沪深A股
   获取股票的code
'''
# 日志
# LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
# logging.basicConfig(filename='parse.log', level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


class Stocks:
    # p 为页数， ps为每页条数.
    url_base = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(BalFlowMain)&sr=-1&p=$$&ps=100&token=894050c76af8597a853f5b408b759f5d&cmd=C._A&sty=DCFFITA&rt=50651072'

    local_file = 'stock.data'

    @classmethod
    def parse_stock_page(self, page):
        # 去掉 ([  ])
        page = page.replace('([', '').replace(')]', '')
        # 转为tuple
        page_groups = page.split('","')
        result = {}
        for stock in page_groups:
            code = stock.split(',')[1]
            name = stock.split(',')[2]
            result[code] = name
        return result

    @classmethod
    def persist_stocks_url(self):
        file_handle = open(self.local_file, 'w')
        for i in range(1, 50):
            url = self.url_base.replace('$$', str(i))
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            stocks_page = response.read().decode('utf-8')
            stock_dict = self.parse_stock_page(stocks_page)
            for (code, name) in stock_dict.items():
                file_handle.write(code + "," + name + "\n")
            file_handle.flush()
            # 最后不满100条时退出执行.
            if (len(stock_dict) < 100):
                logging.info("退出 persist_stocks_url, 当前页数: " + str(i))
                break
        file_handle.close()

    @classmethod
    def get_code_from_file(self):
        if (not os.path.isfile(self.local_file)):
            logging.info(self.local_file + " 文件不存在")
            return None
        file_handle = open('stock.data', 'r')
        stocks_list = file_handle.readlines()
        result = []
        for stock in stocks_list:
            result.append(stock.split(',')[0])
        return result

    @classmethod
    def get_code_from_url(self):
        self.persist_stocks_url()
        return self.get_code_from_file()

    @classmethod
    def get_codes(self):
        codes = self.get_code_from_file()
        if(not codes):
            codes = self.get_code_from_url()
        return codes