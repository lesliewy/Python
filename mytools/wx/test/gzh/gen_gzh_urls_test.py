import unittest

from wx.gzh import gen_gzh_urls


class MyTestCase(unittest.TestCase):
    def test_parse_gzh_list_html(self):
        result = gen_gzh_urls.parse_gzh_list_html("")
        self.assertIsNone(result)

        result = gen_gzh_urls.parse_gzh_list_html("a.txt")
        self.assertIsNone(result)

        result = gen_gzh_urls.parse_gzh_list_html('/Users/leslie/Temp1/2019/0925/每天学点开车技巧.data.html')

    def test_main(self):
        gen_gzh_urls.main()


if __name__ == '__main__':
    unittest.main()
