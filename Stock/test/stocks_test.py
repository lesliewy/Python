import unittest

from download import persist

from Stocks import Stocks


class StocksTest(unittest.TestCase):
    # 验证Stocks.py 中的url是否可用. 同时验证parse_stock_page
    def test_stock_code_url(self):
        dfcf_code_url = Stocks.url_base.replace('$$', '1')
        page = persist.get_response(dfcf_code_url)
        result = Stocks.parse_stock_page(page)
        self.assertTrue(len(result) > 10)

    # 执行会重新生成新的stock.data
    def test_get_code_from_url(self):
        result = Stocks.get_code_from_url()
        self.assertTrue(len(result) > 1000)

    def test_get_code_from_file(self):
        result = Stocks.get_code_from_file()
        self.assertTrue(len(result) > 1000)

