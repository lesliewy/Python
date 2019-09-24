import os
import unittest
from download import sombrero

import constants
from wx.gzh import persist_gzh

url = 'https://mp.weixin.qq.com/s?__biz=MzU3MjE2NzQ4Mg==&mid=2247487542&idx=1&sn=8d8a4d2ba8614cc764052ce97b7dddc8&chksm=fcd45463cba3dd75d6b8f6c1f3e7a12019cca4f8cec04eabf2e2e0e3048b38438d1d0a48d77c&scene=21#wechat_redirect'
article_date = '20180120'
article_full_path = constants.WX_GZH_DATA_DIR + '2018' + '/' + '01' + '/' + 'temp.html'


class MyTestCase(unittest.TestCase):
    def test_persist_gzh_html(self):
        persist_gzh.persist_gzh_html(url, article_date)
        self.assertTrue(os.path.exists(article_full_path))

    def test_get_gzh_title(self):
        persist_gzh.persist_gzh_html(url, article_date)
        soup = sombrero.get_soup_file(article_full_path)
        title = persist_gzh.get_gzh_title(soup)
        self.assertEqual('1个变量，降低至少1倍风险，五步识别多头借贷 | 干货', title)

    def test_process_img(self):
        persist_gzh.persist_gzh_html(url, article_date)
        soup = sombrero.get_soup_file(article_full_path)
        persist_gzh.process_img(soup, article_date)

    def test_can_persist_gzh(self):
        result = persist_gzh.can_persist_gzh();
        self.assertFalse(result)

    def test_persist_gzh_from_file(self):
        persist_gzh.persist_gzh_from_file('')

    def test_main(self):
        persist_gzh.main()


if __name__ == '__main__':
    unittest.main()
