# -*- coding:utf-8 -*-
from DataRetrieve import *

"""
 DataShicimingju测试util
"""
spider = DataShicimingju()

def test_get_categories():
    categories = spider.get_categories()
    for cate in categories:
        print cate

def test_get_authors():
    categories = spider.get_categories()
    authors = spider.get_authors(categories[0])
    for author in authors:
        print author
    print categories[0]

def test_get_author_poems():
    author = {"name" : "屈原", "numofpoems" : 27, "url" : "/chaxun/zuozhe/67.html", "brief" : "", \
              "category" : "先秦"}
    poems = spider.get_author_poems(author)
    if not poems:
        print "没有诗词"
    for poem in poems:
        print poem
    print "total: ", len(poems)

def test_get_poem_content():
    categoryname = "先秦"
    authorname = "屈原"
    poem = {"name" : "九歌 国殇", "url" : "/chaxun/list/7244.html", "precontent" : "", "content" : "", "appreciation" : ""}
    spider.get_poem_content(categoryname, authorname, poem)
    print poem

def test_persist():
    print "aaa"
 


#test_get_categories()
#test_get_authors()
#test_get_author_poems()
test_get_poem_content()