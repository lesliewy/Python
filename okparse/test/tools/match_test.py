import unittest

from tools import match


class MatchTest(unittest.TestCase):

    def test_main(self):
        date_range = "16"
        match.main(date_range)
