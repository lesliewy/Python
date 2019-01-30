import logging
import unittest

from mystring import string_util

# 日志
LOG_FORMAT = "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename='string_utils.log', level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


class StringUtilTest(unittest.TestCase):
    def test_is_any_blank(self):
        self.assertTrue(string_util.is_any_blank(""));
        self.assertTrue(string_util.is_any_blank(" "));
        self.assertTrue(string_util.is_any_blank("", ""));
        self.assertTrue(string_util.is_any_blank("a", ""));
        self.assertTrue(string_util.is_any_blank(" ", "b"));
        self.assertFalse(string_util.is_any_blank(" a", "b"));
