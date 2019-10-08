import unittest

from utils import match_utils


class MatchUtilsTest(unittest.TestCase):

    def test_get_match_result(self):
        self.assertEqual("", match_utils.get_match_result("", ""));
        self.assertEqual("", match_utils.get_match_result("", "3"));
        self.assertEqual("", match_utils.get_match_result("3", ""));
        self.assertEqual("胜", match_utils.get_match_result("3", "1"));
        self.assertEqual("平", match_utils.get_match_result("3", "3"));
        self.assertEqual("负", match_utils.get_match_result("3", "4"));
