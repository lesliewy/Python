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
        a, b, c = financial_report_query.trans_money("1,234,2", "2,3", "--")
        self.assertEqual(12342, a);
        self.assertEqual(23, b)
        self.assertEqual("--", c)

    def test_get_zc(self):
        financial_report_query.assign_dict("002769")
        hbzj, zxjlzc, zzc, jzc, gdzc, ch, sy, yspj, yszk = financial_report_query.get_zc("20171231")
        self.assertEqual((1188926, 1233399, 1397533, 126085, 816, 10772, '--', 134, 96705),
                         (hbzj, zxjlzc, zzc, jzc, gdzc, ch, sy, yspj, yszk))

    def test_get_fz(self):
        financial_report_query.assign_dict("600167")
        zfz, cqjk, dqjk, yfzq, yxfz, cqdysyfz = financial_report_query.get_fz("20171231")
        self.assertEqual((zfz, cqjk, dqjk, yfzq, yxfz, cqdysyfz), (397716, 8893, '--', '--', 8893, 229927))

    def test_get_lr(self):
        financial_report_query.assign_dict("600697")
        yyzsr, yylr, lrze, jlr = financial_report_query.get_lr("20171231")
        self.assertEqual((yyzsr, yylr, lrze, jlr), (1398142, 82540, 84445, 61049))

    def test_get_xjll(self):
        financial_report_query.assign_dict("600697")
        zyhdxjllje, = financial_report_query.get_xjll("20171231")
        self.assertEqual((166065,), (zyhdxjllje,))