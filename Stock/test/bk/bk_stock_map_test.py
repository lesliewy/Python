import os.path
import unittest

import Constants
from bk import bk_stock_map


class MyTestCase(unittest.TestCase):
    def test_get_industry_notion_raw(self):
        result = bk_stock_map.get_industry_notion_raw()
        self.assertIsNotNone(result)

    def test_get_industry_json(self):
        result = bk_stock_map.get_industry_notion_json('行业')
        self.assertIsNotNone(result)

        result = bk_stock_map.get_industry_notion_json('概念')
        self.assertIsNotNone(result)

        result = bk_stock_map.get_industry_notion_json('adjisji')
        self.assertIsNone(result)

    def test_get_all_industries(self):
        result = bk_stock_map.get_all_industries()
        self.assertTrue(result is not None and len(result) > 20)

    def test_get_all_notions(self):
        result = bk_stock_map.get_all_notions()
        self.assertTrue(result is not None and len(result) > 20)

    def test_get_boards_stocks(self):
        result = bk_stock_map.get_board_stocks("   ")
        self.assertIsNone(result)

        result = bk_stock_map.get_board_stocks("001")
        self.assertIsNone(result)

        result = bk_stock_map.get_board_stocks("BK0689")
        self.assertGreater(len(result), 50)

    def test_persist_boards_stocks(self):
        bk_stock_map.persist_boards_stocks()
        self.assertTrue(os.path.exists(Constants.DATA_PATH + '/' + 'industry.json'))
        self.assertTrue(os.path.exists(Constants.DATA_PATH + '/' + 'notion.json'))

    def test_get_industry_by_code(self):
        result = bk_stock_map.get_industry_by_code('000001')
        self.assertEqual('银行', result)

        result = bk_stock_map.get_industry_by_code('300604')
        self.assertEqual('专用设备', result)

    def test_get_notions_by_code(self):
        result = bk_stock_map.get_notions_by_code('000001')
        self.assertEqual(['MSCI大盘', '深证100R', '转债标的'], result)

        result = bk_stock_map.get_notions_by_code('300604')
        self.assertEqual(['国产芯片', '养老金'], result)


if __name__ == '__main__':
    unittest.main()
