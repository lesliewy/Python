import unittest

from mystring import string_util


class StringUtilTest(unittest.TestCase):
    def test_is_any_blank(self):
        self.assertTrue(string_util.is_any_blank(""));
        self.assertTrue(string_util.is_any_blank(" "));
        self.assertTrue(string_util.is_any_blank("", ""));
        self.assertTrue(string_util.is_any_blank("a", ""));
        self.assertTrue(string_util.is_any_blank(" ", "b"));
        self.assertFalse(string_util.is_any_blank(" a", "b"));
