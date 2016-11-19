# -*- coding:utf-8 -*-
from Mongo import *

"""
 mongodb 查询操作.
"""
class DBQuery(object):

    # 查询某位诗人的诗词总数. authorurl 用于防止同一年代同名诗人.
    @classmethod
    def authorpoemscount(self, categoryname, authorname, authorurl):
        # 这种方式调用, 必须使用 from import 来引入.
        db = Mongo(database='poetry')
        return db.poem.find({"category.name" : categoryname, "author.name" : authorname, "author.url": authorurl}).count()

    # 查询某位诗人某首诗是否存在.
    @classmethod
    def authorpoemcount(self, categoryname, authorname, poemname, poemurl):
        db = Mongo(database='poetry')
        return db.poem.find({"category.name" : categoryname, "author.name" : authorname, "poems.name" : poemname, "poems.url" : poemurl}).count()

    # 查询某位诗人的诗词列表.
    @classmethod
    def authorpoems(self, categoryname, authorname, authorurl):
        db = Mongo(database='poetry')
        return db.poem.find({"category.name" : categoryname, "author.name" : authorname, "author.url" : authorurl}, {"poems" : 1})