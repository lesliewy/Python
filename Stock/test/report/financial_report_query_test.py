import logging
import unittest

from report import financial_report_query

# 日志
LOG_FORMAT = "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename='query.log', level=logging.INFO, format=LOG_FORMAT,
                    datefmt=DATE_FORMAT)


class FinancialReportQueryTest(unittest.TestCase):
    def test_trans_money(self):
        a, b, c, d, e = financial_report_query.trans_money("1,234,2", "2,3", "--", "-2,320", "-87")
        self.assertEqual(12342, a);
        self.assertEqual(23, b)
        self.assertEqual("--", c)
        self.assertEqual(-2320, d)
        self.assertEqual(-87, e)

    def test_get_latest_season_date(self):
        self.assertEqual("20171231", financial_report_query.get_latest_season_date(2018, 2))
        self.assertEqual("20180331", financial_report_query.get_latest_season_date(2018, 5))
        self.assertEqual("20180630", financial_report_query.get_latest_season_date(2018, 7))
        self.assertEqual("20171231", financial_report_query.get_latest_season_date(2018, 3))
        self.assertEqual("20180930", financial_report_query.get_latest_season_date(2018, 10))

    def test_get_last_season_date(self):
        self.assertEqual("20171231", financial_report_query.get_last_season_date("20180331"))
        self.assertEqual("20180331", financial_report_query.get_last_season_date("20180630"))
        self.assertEqual("20180630", financial_report_query.get_last_season_date("20180930"))
        self.assertEqual("20180930", financial_report_query.get_last_season_date("20181231"))
        self.assertNotEqual("20171231", financial_report_query.get_last_season_date("20180322"))

    def test_get_last_year_report_date(self):
        self.assertEqual("20171231", financial_report_query.get_last_year_report_date("20181231"))
        self.assertEqual("20130630", financial_report_query.get_last_year_report_date("20140630"))
        self.assertTrue(None == financial_report_query.get_last_year_report_date("--"))

    def test_get_zc(self):
        financial_report_query.assign_dict("002769")
        hbzj, zxjlzc, zzc, jzc, gdzc, ch, sy, yspj, yszk = financial_report_query.get_zc("20171231")
        self.assertEqual((1188926, 1233399, 1397533, 126085, 816, 10772, '--', 134, 96705),
                         (hbzj, zxjlzc, zzc, jzc, gdzc, ch, sy, yspj, yszk))

    def test_get_fz(self):
        financial_report_query.assign_dict("600167")
        zfz, cqjk, dqjk, yfzq, yxfz, cqdysyfz, ynndqfldfz, fzzh = financial_report_query.get_fz("20171231")
        self.assertEqual((397716, 8893, '--', '--', 8893, 229927, '--', 8893),
                         (zfz, cqjk, dqjk, yfzq, yxfz, cqdysyfz, ynndqfldfz, fzzh))

    def test_get_lr(self):
        financial_report_query.assign_dict("600697")
        yyzsr, yylr, lrze, jlr = financial_report_query.get_lr("20171231")
        self.assertEqual((yyzsr, yylr, lrze, jlr), (1398142, 82540, 84445, 61049))

    def test_get_xjll(self):
        financial_report_query.assign_dict("600697")
        zyhdxjllje, xssptglwxj = financial_report_query.get_xjll("20171231")
        self.assertEqual((166065, 1491765), (zyhdxjllje, xssptglwxj))
