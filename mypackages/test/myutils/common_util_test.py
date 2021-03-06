import logging
import unittest

from myutils import common_util

# 日志
LOG_FORMAT = "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename='myutils.log', level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


class CommonUtilTest(unittest.TestCase):
    def test_is_any_none(self):
        self.assertFalse(common_util.is_any_none({}));
        self.assertFalse(common_util.is_any_none(""));
        self.assertFalse(common_util.is_any_none("", {}, []));
        self.assertFalse(common_util.is_any_none([1], {"a": 2}));
        self.assertTrue(common_util.is_any_none(None));
        self.assertTrue(common_util.is_any_none(None, None, None));
        self.assertTrue(common_util.is_any_none({"a": 1}, None))
        self.assertTrue(common_util.is_any_none(None, None, [1, 2, 3]))

    def test_cal_percent(self):
        self.assertEqual("50.0%", common_util.cal_percent(1, 2))
        self.assertEqual("56.52%", common_util.cal_percent(13, 23))
        self.assertEqual("5.5962%", common_util.cal_percent(130, 2323, 4))
        self.assertEqual("100.0%", common_util.cal_percent(10, 5, increase="Y"))
        self.assertEqual("150.0%", common_util.cal_percent(10, 4, increase="Y"))
        self.assertEqual("42.86%", common_util.cal_percent(10, 7, increase="Y"))
        self.assertEqual("-50.0%", common_util.cal_percent(10, 20, increase="Y"))

    def test_format_table(self):
        header_tup = None
        value_tups = None
        header_format_str = ""
        value_format_str = ""
        format_table = common_util.format_table(header_tup, value_tups, header_format_str, value_format_str);
        self.assertEqual(None, format_table)

        header_tup = ()
        value_tups = []
        format_table = common_util.format_table(header_tup, value_tups, header_format_str, value_format_str);
        self.assertEqual(None, format_table)

        header_tup = ("报告日期", "总资产", "总负债", "总负债/总资产")
        value_tups = [("20171231", 123, 23, common_util.cal_percent(123, 23))]
        header_format_str = '{0[0]:>10}{0[1]:>10}{0[2]:>10}{0[3]:>10}'
        value_format_str = '{0[0]:>13}{0[1]:>12}{0[2]:>12}{0[3]:>14}'
        format_table = common_util.format_table(header_tup, value_tups, header_format_str, value_format_str);
        logging.info(format_table)

        value_tups = [("20190331", 1231234, -232222, common_util.cal_percent(1231234, -232222)),
                      ("20190631", 88777889, 23288, common_util.cal_percent(88777889, 23288))]
        format_table = common_util.format_table(header_tup, value_tups, header_format_str, value_format_str);
        logging.info(format_table)

    def test_format_table_dict(self):
        val_dict = {"000001_中国平安": "2.3%", "600231_烽火通信": "28%", "600832_益生股份": "8.9%", "000321_格力电器": "43.6%",
                    "600888_美的集团": "19.7%"}
        logging.info("\n" + common_util.format_table_dict(val_dict, 5))
