import unittest

from download import persist

from research_report import lt_research_report


class MyTestCase(unittest.TestCase):
    # 测试研报的url是否可用.
    def test_research_report_url(self):
        resp = persist.get_response(lt_research_report.research_report_url.replace('$$', '000001'))
        self.assertTrue(len(resp) > 500)

    def test_parse_research_report(self):
        lt_research_report.parse_research_report('000001')



if __name__ == '__main__':
    unittest.main()
