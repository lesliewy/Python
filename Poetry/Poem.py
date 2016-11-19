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
        return "name=" + self.name  + ", " + "url=" + self.url + ", " + "tags=" + self.gettags() + ", "\
                + "content:" + self.content + ", "  \
                + "appreciation:" + self.appreciation

    def gettags(self):
        tags = ""
        for tag in tags:
            tags += " " + tag
        return tags

