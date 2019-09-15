import os.path
import unittest

import Constants
from bk import industry


class MyTestCase(unittest.TestCase):
    def test_get_industry_notion_raw(self):
        result = industry.get_industry_notion_raw()
        self.assertIsNotNone(result)

    def test_get_industry_json(self):
        result = industry.get_industry_notion_json('行业')
        self.assertIsNotNone(result)

        result = industry.get_industry_notion_json('概念')
        self.assertIsNotNone(result)

        result = industry.get_industry_notion_json('adjisji')
        self.assertIsNone(result)

    def test_get_all_industries(self):
        result = industry.get_all_industries()
        self.assertTrue(result is not None and len(result) > 20)

    def test_get_all_notions(self):
        result = industry.get_all_notions()
        self.assertTrue(result is not None and len(result) > 20)

    def test_get_boards_stocks(self):
        result = industry.get_board_stocks("   ")
        self.assertIsNone(result)

        result = industry.get_board_stocks("001")
        self.assertIsNone(result)

        result = industry.get_board_stocks("BK0689")
        self.assertGreater(len(result), 50)

    def test_persist_boards_stocks(self):
        industry.persist_boards_stocks()
        self.assertTrue(os.path.exists(Constants.DATA_PATH + '/' + 'industry.json'))
        self.assertTrue(os.path.exists(Constants.DATA_PATH + '/' + 'notion.json'))


if __name__ == '__main__':
    unittest.main()
