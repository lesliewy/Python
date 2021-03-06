import os
import unittest

from analysis import match_summary

# data 目录
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'data')


class MyTestCase(unittest.TestCase):
    def test_get_data_from_match_dat(self):
        match_dat_file = ''
        self.assertIsNone(match_summary.get_data_from_match_dat(match_dat_file))

        match_dat_file = 'a'
        self.assertIsNone(match_summary.get_data_from_match_dat(match_dat_file))

        match_dat_file = os.path.join(DATA_DIR, '160302/match.dat')
        mat = match_summary.get_data_from_match_dat(match_dat_file, exclude_unopen=False)
        self.assertEqual('江苏苏宁', mat[3][1])
        self.assertEqual(4, mat[0]['host_goals'])
        self.assertTrue(len(mat['visiting_name']) == 528)

    def test_desc(self):
        match_dat_file = os.path.join(DATA_DIR, '160301/match.dat')
        match_summary.desc(match_dat_file)
