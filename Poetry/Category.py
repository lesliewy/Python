# -*- coding:utf-8 -*-

"""
 年代 对象. 存储年代信息(http://www.shicimingju.com/左侧的年代诗人)
"""
class Category:
    name = ""
    url = ""
    numofauthors = 0

    # 内置方法，方便输出.
    def __str__(self):
        return "name=" + self.name.encode('utf-8') + ", " + "url=" + self.url + ", " \
                + "numofauthors:" + str(self.numofauthors)
