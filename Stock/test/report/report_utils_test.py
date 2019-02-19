import unittest

from report import report_utils


class ReportUtilsTest(unittest.TestCase):
    def test_trans_money(self):
        a, b, c, d, e = report_utils.trans_money("1,234,2", "2,3", "--", "-2,320", "-87")
        self.assertEqual(12342, a);
        self.assertEqual(23, b)
        self.assertEqual("--", c)
        self.assertEqual(-2320, d)
        self.assertEqual(-87, e)

    def test_get_latest_season_date(self):
        self.assertEqual("20171231", report_utils.get_latest_season_date(2018, 2))
        self.assertEqual("20180331", report_utils.get_latest_season_date(2018, 5))
        self.assertEqual("20180630", report_utils.get_latest_season_date(2018, 7))
        self.assertEqual("20171231", report_utils.get_latest_season_date(2018, 3))
        self.assertEqual("20180930", report_utils.get_latest_season_date(2018, 10))

    def test_get_last_season_date(self):
        self.assertEqual("20171231", report_utils.get_last_season_date("20180331"))
        self.assertEqual("20180331", report_utils.get_last_season_date("20180630"))
        self.assertEqual("20180630", report_utils.get_last_season_date("20180930"))
        self.assertEqual("20180930", report_utils.get_last_season_date("20181231"))
        self.assertNotEqual("20171231", report_utils.get_last_season_date("20180322"))

    def test_get_last_year_report_date(self):
        self.assertEqual("20171231", report_utils.get_last_year_report_date("20181231"))
        self.assertEqual("20130630", report_utils.get_last_year_report_date("20140630"))
        self.assertTrue(None == report_utils.get_last_year_report_date("--"))
