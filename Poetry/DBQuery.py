# -*- coding:utf-8 -*-
from Mongo import *

"""
 mongodb 查询操作.
"""
class DBQuery(object):

    @classmethod
    def allauthorpoems(self):
        # 这种方式调用, 必须使用 from import 来引入.
        db = Mongo()
