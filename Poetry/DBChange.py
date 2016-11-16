# -*- coding:utf-8 -*-
from Mongo import *
from Category import *
from Author import *
from Poem import *

"""
 mongodb 修改操作.
"""
class DBChange(object):

    @classmethod
    def persist(self, category, author, poem):
        # 这种方式调用, 必须使用 from import 来引入.
        db = Mongo(database='poetry')
        db.poem.insert_one(
            {
                "category": {
                    "name": category.name,
                    "url": category.url,
                    "numofauthors": category.numofauthors
                },
                "author": {
                    "name": author.name,
                    "url": author.url,
                    "numofpoems": author.numofpoems,
                    "brief": author.brief
                },
                "poems": [
                    {
                        "name": poem.name,
                        "url": poem.url,
                        "precontent": poem.precontent,
                        "content": content,
                        "tags": poem.tags,
                        "appreciation": poem.appreciation
                    }
                ]
            }
        )
    @classmethod
    def updateauthorpoems(self, categoryname, authorname, authorurl, poems):
        db = Mongo(database='poetry')
        db.poem.update_one(
            {"category.name": categoryname, "author.name": authorname},
            {"$set": {"poems": poems}}
        )

