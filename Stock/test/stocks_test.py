import unittest

from download import persist

from Stocks import Stocks


class StocksTest(unittest.TestCase):
    # 验证Stocks.py 中的url是否可用.
    def test_stock_code_url(self):
        dfcf_code_url = Stocks.url_base.replace('$$', '1')
        page = persist.get_response(dfcf_code_url)
        result = Stocks.parse_stock_page(page)
        self.assertTrue(len(result) > 10)
