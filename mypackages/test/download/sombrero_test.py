import logging
import unittest

from download import sombrero

# 日志
LOG_FORMAT = "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename='sombrero.log', level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


class SombreroTest(unittest.TestCase):
    soup_file = None;

    url_baike_chaodai = "";
    file_path_baike_chaodai = "";

    url_baike_xiangsheng = "";
    file_path_baike_xiangsheng = "";

    data_for_adjust_architecture = {};

    @classmethod
    def setUpClass(cls):
        print("this is setUpClass...");
        cls.url_baike_chaodai = "https://baike.baidu.com/item/%E6%9C%9D%E4%BB%A3/7716136";
        cls.file_path_baike_chaodai = "/Users/leslie/MyProjects/Data/Stock/report/chaodai.html";

        cls.url_baike_xiangsheng = "https://baike.baidu.com/item/%E7%9B%B8%E5%A3%B0";
        cls.file_path_baike_xiangsheng = "/Users/leslie/MyProjects/Data/Stock/report/xiangsheng.html";

        cls.data_for_adjust_architecture = {"第一代": {"大家": "张三禄"},
                                            "第二代": {"大家": "朱绍文", "小家": "阿彦涛、沈春和"},
                                            "第三代": {"大家": "恩绪、高闻元", "小家": "徐长福、桂祯"},
                                            "第四代": {"大家": "相声八德", "小家": "郭瑞林、李瑞丰、张杰尧"},
                                            "第五代": {"大家": "张寿臣、马三立", "小家": "于俊波、郭启儒"},
                                            "第六代": {"大家": "赵佩茹、常宝堃", "小家": "李洁尘、杨绍奎"},
                                            "第七代": {"大家": "石富宽、马季", "小家": "朱文正"},
                                            "第八代": {"大家": "于谦、孙越、侯震", "小家": "杨贵田"},
                                            "第一代 - 第三代": {"arch中包含": "删除"}
                                            };

    def setUp(self):
        print("this is setUp...");

    def tearDown(self):
        print("this is tearDown...");
        if (self.soup_file):
            self.soup_file.close();

    @classmethod
    def tearDownClass(cls):
        print("this is tearDownClass...");

    def test_get_content_with_selector(self):
        self.soup_file, soup = sombrero.get_soup(self.url_baike_chaodai, self.file_path_baike_chaodai);
        selector0 = "";
        result0 = sombrero.get_content_with_selector(soup, selector0);
        self.assertIsNone(result0, "必输项校验不通过");

        content1 = "奴隶社会";
        selector1 = "body > div.body-wrapper > div.content-wrapper > div > div.main-content > div:nth-of-type(17) > a > b";
        result1 = sombrero.get_content_with_selector(soup, selector1);
        self.assertEqual(content1, result1, content1 + "不匹配");

    def test_get_num_of_child(self):
        self.soup_file, soup = sombrero.get_soup(self.url_baike_chaodai, self.file_path_baike_chaodai);
        num_of_links2 = 4;
        selector2 = "body > div.body-wrapper > div.content-wrapper > div > div.main-content > div:nth-of-type(25)";
        child_type = "a";
        result2 = sombrero.get_num_of_child(soup, selector2, child_type)
        self.assertEqual(num_of_links2, result2, "东周下的a标签个数不匹配.")

        selector3 = "body > div.wgt-footer-main";
        child_type = "div";
        num_of_div3 = 2;
        result2 = sombrero.get_num_of_child(soup, selector3, child_type);
        self.assertEqual(num_of_div3, result2, "div 标签个数不匹配");

    def test_get_line_or_column_recursion(self):
        self.soup_file, soup = sombrero.get_soup(self.url_baike_xiangsheng, self.file_path_baike_xiangsheng);

        # selector1 = 'body > div.body-wrapper > div.content-wrapper > div > div.main-content > table:nth-of-type(10) > tbody > tr:nth-of-type(61) > td:nth-of-type(2)';
        selector1 = 'body > div.body-wrapper > div.content-wrapper > div > div.main-content > table:nth-of-type(10) > tbody > tr';
        content1 = "郭德纲";
        key_dict, concat_content = sombrero.get_line_or_column_recursion(soup, selector1, location="H", seq_num=60);
        self.assertTrue(content1 in str(concat_content), "郭德纲不在该selector中");

    def test_get_key(self):
        self.soup_file, soup = sombrero.get_soup(self.url_baike_xiangsheng, self.file_path_baike_xiangsheng);
        selector1 = "body > div.body-wrapper > div.content-wrapper > div > div.main-content > table:nth-of-type(10) > tbody > tr";
        result1 = sombrero.get_key(soup, selector1, key_location="H", key_seq=0);
        self.assertEqual("第七代", result1[0], "key中第一列不匹配.")
        self.assertEqual("第八代", result1[1], "key中第二列不匹配.")

        selector2 = "body > div.body-wrapper > div.content-wrapper > div > div.main-content > table:nth-of-type(12) > tbody > tr"
        result2 = sombrero.get_key(soup, selector2, key_location="V", key_seq=0);
        self.assertEqual("台北曲艺团", result2[1], "key获取失败，台湾地区相声演员");

    def test_get_value1(self):
        self.soup_file, soup = sombrero.get_soup(self.url_baike_xiangsheng, self.file_path_baike_xiangsheng);
        selector1 = "body > div.body-wrapper > div.content-wrapper > div > div.main-content > table:nth-of-type(10) > tbody > tr";
        result1 = sombrero.get_value(soup, selector1, exclude_top=True);
        self.assertTrue("于谦" in result1[2][1]);
        self.assertTrue("马季" in result1[3][0]);
        self.assertTrue("赵伟洲" in result1[11][1]);

        ### 将列转为key的名称
        column_selector2 = "body > div.body-wrapper > div.content-wrapper > div > div.main-content > table:nth-of-type(10) > tbody > tr";
        column_dict2 = sombrero.get_key(soup, column_selector2, key_location="H", key_seq=0);
        result2 = sombrero.get_value(soup, selector1, exclude_top=True, colume_key_dict=column_dict2);
        colume_key_1 = "第七代"
        colume_key_2 = "第八代"
        self.assertTrue("于谦" in result2[2][colume_key_2]);
        self.assertTrue("马季" in result2[3][colume_key_1]);
        self.assertTrue("赵伟洲" in result2[11][colume_key_2]);

    def test_get_value2(self):
        self.soup_file, soup = sombrero.get_soup(self.url_baike_xiangsheng, self.file_path_baike_xiangsheng);
        line_selector1 = "body > div.body-wrapper > div.content-wrapper > div > div.main-content > table:nth-of-type(12) > tbody > tr";
        line_key_dict1 = sombrero.get_key(soup, line_selector1, key_location="V", key_seq=0);
        result1 = sombrero.get_value(soup, line_selector1, exclude_top=False, exclude_left=True,
                                     line_key_dict=line_key_dict1);
        line_key_1 = "台北曲艺团"
        line_key_2 = "相声瓦舍"
        self.assertTrue("刘增锴" in result1[line_key_1][0]);
        self.assertTrue("冯翊纲" in result1[line_key_2][0]);

    def test_adjust_architecture1(self):
        key1 = "第一代 - 第三代";
        arch_template = {key1: ["第一代", "第二代", "第三代"]}
        result1 = sombrero.adjust_architecture_dict(arch_template, self.data_for_adjust_architecture);
        self.assertIn("第一代", result1[key1], key1 + " 的值不对.");
        self.assertIn("第二代", result1[key1], key1 + " 的值不对.");
        self.assertIn("第三代", result1[key1], key1 + " 的值不对.");
        self.assertIn("第四代", result1, "result1 的值不对.");

        key2 = "第五代 - 第七代";
        arch_template = {key1: ["第一代", "第二代", "第三代"], key2: ["第五代", "第六代", "第七代"]}
        result2 = sombrero.adjust_architecture_dict(arch_template, self.data_for_adjust_architecture);
        self.assertIn("第一代", result2[key1], key1 + " 的值不对.");
        self.assertIn("第二代", result2[key1], key1 + " 的值不对.");
        self.assertIn("第三代", result2[key1], key1 + " 的值不对.");
        self.assertIn("第四代", result2, "result2 的值不对.");
        self.assertIn("第五代", result2[key2], "result2 的值不对.");
        self.assertIn("第六代", result2[key2], "result2 的值不对.");

    def test_adjust_architecture2(self):
        arch_template = {"1-3": ["第一代", "第二代", "第三代"], "5-8": {"5&&8": ["第五代", "第八代"], "6-7": ["第六代", "第七代"]}}
        result1 = sombrero.adjust_architecture_dict(arch_template, self.data_for_adjust_architecture);
        self.assertIn("第一代", result1["1-3"], "值不对.");
        self.assertIn("第二代", result1["1-3"], "值不对.");
        self.assertIn("第三代", result1["1-3"], "值不对.");
        self.assertIn("第四代", result1, "值不对.");
        self.assertIn("第五代", result1["5-8"]["5&&8"], "值不对.");
        self.assertIn("第六代", result1["5-8"]["6-7"], "值不对.");

    def test_adjust_architecture3(self):
        arch_template = {"1-3": ["第一代", "第二代", "第三代"],
                         "5-8": {"5&&8": ["第五代", "第八代"], "6-7": {"6": ["第六代"], "7": ["第七代"]}}}
        result1 = sombrero.adjust_architecture_dict(arch_template, self.data_for_adjust_architecture);
        self.assertIn("第一代", result1["1-3"], "值不对.");
        self.assertIn("第二代", result1["1-3"], "值不对.");
        self.assertIn("第三代", result1["1-3"], "值不对.");
        self.assertIn("第四代", result1, "值不对.");
        self.assertIn("第五代", result1["5-8"]["5&&8"], "值不对.");
        self.assertIn("第六代", result1["5-8"]["6-7"]["6"], "值不对.");
