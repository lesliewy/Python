# -*- coding:utf-8 -*-
import urllib
import urllib2
# from import 方式引入的，使用时可以省略module名
from bs4 import BeautifulSoup
from Author import *
from Category import *

# 解析诗词名句网(http://www.shicimingju.com/)的信息.


class DataShicimingju:
    def __init__(self):
        self.URL = "http://www.shicimingju.com"


    # 获取年代. http://www.shicimingju.com/左侧的年代诗人.
    # 返回值形式 {"先秦":"/category/xianqinshiren"}
    def get_categories(self):
        try:
            # 构建请求的request
            request = urllib2.Request(self.URL)
            # 利用urlopen获取页面代码
            response = urllib2.urlopen(request)
            # 将页面转化为UTF-8编码
            agepage = response.read()
            if not agepage:
                print u"获取年代信息页面出错."
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接诗词名句网失败,错误原因", e.reason
                return None

        categories = []

        soup = BeautifulSoup(agepage)
        allcates = soup.select("#left > div:nth-of-type(1) > ul > li")
        for cate in allcates:
            atag = cate.select("a")
            catename = atag[0].string
            cateurl = atag[0]["href"]
            category = Category()
            category.name = catename
            category.url = cateurl
            categories.append(category)
        return categories
        
    # 获取年代内的诗人. http://www.shicimingju.com/category/xianqinshiren
    def get_authors(self, categoryurl):
        print "categoryurl: ", categoryurl
        if not categoryurl:
            print "categoryurl is empty, return now..."
            return 
        authorsurl = self.URL + categoryurl
        try:
            request = urllib2.Request(authorsurl)
            response = urllib2.urlopen(request)
            authorspage = response.read().decode('utf-8')
            if not authorspage:
                print u"获取诗人页面出错."
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"获取诗人页面失败,错误原因", e.reason
                return None
        authors = []
        soup = BeautifulSoup(authorspage)
        # #middlediv > div > div > ul > li:nth-child(1) > a > span
        allauthors = soup.select("#middlediv > div > div > ul > li")
        for author in allauthors:
            atag = author.select("a")
            # tag 的 .content 属性可以将tag的子节点以列表的方式输出, 而.children返回一个 list 生成器对象,使用
            # for child in  soup.body.children: 这种方式
            authorname = atag[0].contents[0]
            authorurl = atag[0]["href"]
            # 最后需要去掉前后()
            numofpoems = atag[0].contents[1].string[1:-1]
            author = Author()
            author.name = authorname
            author.url = authorurl
            author.numofpoems = numofpoems
            authors.append(author)
        return authors

spider = DataShicimingju()

categories = spider.get_categories()
for cate in categories:
    print cate

authors = spider.get_authors(categories[0].url)
for author in authors:
    print author