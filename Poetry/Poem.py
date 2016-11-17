# -*- coding:utf-8 -*-

"""
 poem 对象. 存储poem页面(http://www.shicimingju.com/chaxun/list/6856.html)相关信息
"""
class Poem:
    # 名字
    name = ""

    # 所在的url
    url = ""

    # 正文
    content = ""

    # 标签
    tags = []

    # 作品赏析
    appreciation = ""

    # 内置方法，方便输出.
    def __str__(self):
        return "name=" + self.name.encode('utf-8')  + ", " + "url=" + self.url + ", " \
                + "content:" + self.content.encode('utf-8') + ", "  \
                + "appreciation:" + self.appreciation.encode('utf-8')
