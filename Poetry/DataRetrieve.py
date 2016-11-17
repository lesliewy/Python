# -*- coding:utf-8 -*-
import urllib
import urllib2
import string
import re
# from import 方式引入的，使用时可以省略module名
from bs4 import BeautifulSoup
from Author import *
from Category import *
from DBQuery import *
from Poem import *

"""
 解析诗词名句网(http://www.shicimingju.com/)的信息, 并存入mongodb
"""
class DataShicimingju:
    def __init__(self):
        self.URL = "http://www.shicimingju.com"
        self.timeout = 5

    # 获取年代. http://www.shicimingju.com/左侧的年代诗人.
    # 返回值形式 {"先秦":"/category/xianqinshiren"}
    def get_categories(self):
        try:
            # 构建请求的request
            request = urllib2.Request(self.URL)
            # 利用urlopen获取页面代码
            response = urllib2.urlopen(request, timeout = self.timeout)
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
    def get_authors(self, category):
        categoryurl = category.url
        print "categoryurl: ", categoryurl
        if not categoryurl:
            print "categoryurl is empty, return now..."
            return None
        authorsurl = self.URL + categoryurl
        try:
            request = urllib2.Request(authorsurl)
            response = urllib2.urlopen(request, timeout = self.timeout)
            authorspage = response.read().decode('utf-8')
            if not authorspage:
                print u"获取诗人页面出错."
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"获取诗人页面失败,错误原因", e.reason
                return None
        authors = []
        soup = BeautifulSoup(authorspage)
        # 年代内的诗人数目. #niandai_title
        catetitle = unicode(soup.select("#niandai_title")[0].string)

        numofauthors = string.atoi(catetitle[catetitle.index("(") + 1:-2].encode('utf-8'))
        category.numofauthors = numofauthors
        allauthors = soup.select("#middlediv > div > div > ul > li")
        for author in allauthors:
            atag = author.select("a")
            # tag 的 .content 属性可以将tag的子节点以列表的方式输出, 而.children返回一个 list 生成器对象,使用
            # for child in  soup.body.children: 这种方式
            authorname = atag[0].contents[0]
            authorurl = atag[0]["href"]
            # 最后需要去掉前后()
            numofpoems = string.atoi(atag[0].contents[1].string[1:-1])
            author = Author()
            author.name = authorname
            author.url = authorurl
            author.numofpoems = numofpoems
            authors.append(author)
        return authors

    # 获取某个作者的所有诗列表.
    def get_author_poems(self, categoryname, author):
        print author
        # {"name" : "aa", "numofpoems" : 27, "url" : "/chaxun/zuozhe/67.html"} 这样构造author, 这种赋值方式只能使用
        # author["name"]来访问，不可以author.name,因为Author中没有 __getitem__方法. 而dict中有.
        authorname = author.name
        authorurl = author.url
        numofpoems = author.numofpoems
        # 查询是否已经全部存在
        # 这种方式调用必须使用from import方式引入.
        existednum = DBQuery.authorpoemscount(categoryname, authorname, authorurl)
        if(existednum == numofpoems):
            print "已存在", authorname, "的", numofpoems, "首诗."
            return None

        fullauthorurl = self.URL + authorurl
        allpoems = []
        # 循环多次，直到错误页面.
        i = 0
        while i <= 1000:
            i += 1
            print i
            if(i > 1):
                fullauthorurl = fullauthorurl.replace(".html", "_" + str(i) + ".html")

            try:
                request = urllib2.Request(fullauthorurl)
                response = urllib2.urlopen(request, timeout = self.timeout)
                authorpage = response.read().decode('utf-8')
                if not authorpage:
                    print u"获取", authorname, "诗列表出错:", fullauthorurl
                    return allpoems
            except urllib2.URLError, e:
                if hasattr(e, "reason"):
                    print "获取", authorname, "诗列表页面失败:", fullauthorurl, " 错误原因", e.reason, \
                          " 可能已经获取完毕"
                return allpoems
            soup = BeautifulSoup(authorpage)
            # 诗人简介
            brief = ""
            if(i == 1):
                brieftext = soup.select("#middlediv > div.jianjie.yuanjiao > div ")
                # 有的不存在简介.
                if brieftext:
                    allbrief = str(brieftext[0])
                    pattern = re.compile('.*?<img.*?/>(.*?)</div>', re.S)        
                    matchobj = re.search(pattern, allbrief)
                    if matchobj:
                        print "not empty."
                        brief = matchobj.group(1).strip()
                        author.brief = brief
                print "brief:", brief
            # 诗列表 #chaxun_miao > div.shicilist > ul:nth-child(1)
            allpoemtext = soup.select("#chaxun_miao > div.shicilist > ul")
            if not allpoemtext:
                print "没有诗存在，返回"
                return None
            for poemul in allpoemtext:
                poem = Poem()
                line1 = poemul.select("> li:nth-of-type(1) > a")
                poem.url = line1[0]["href"]
                poem.name = line1[0].string
                allpoems.append(poem)
        return allpoems

    # 获取诗词正文.
    def get_poem_content(self, categoryname, authorname, poem):
        print poem
        poemname = poem.name
        poemurl = poem.url
        # 查询是否已经存在
        existednum = DBQuery.authorpoemcount(categoryname, authorname, poemname, poemurl)
        print "existednum: ", existednum
        if(existednum > 0):
            print "已存在", authorname, "的", poemname
            return None

        fullpoemurl = self.URL + poemurl
        try:
            request = urllib2.Request(fullpoemurl)
            response = urllib2.urlopen(request, timeout = self.timeout)
            poempage = response.read().decode('utf-8')
            if not poempage:
                print u"获取诗正文页面出错."
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"获取诗正文失败:",  fullpoemurl, " 错误原因", e.reason
                return None
        soup = BeautifulSoup(poempage)
        # 诗词内容 #shicineirong
        originalcontent = soup.select("#shicineirong")[0].contents
        content = ""
        for contenttemp in originalcontent:
            # navigatablestring 需要先encode.
            content += contenttemp.encode('utf-8')
        # 分类标签 #middlediv > div.zhuti.yuanjiao > div.listscmk > a:nth-child(1)
        tags = []
        tagstext = soup.select("#middlediv > div.zhuti.yuanjiao > div.listscmk > a")
        if tagstext:
            for tag in tagstext:
                tags.append(tag.string)
        # 赏析 #middlediv > div:nth-child(2)
        appreciation = ""
        originalappreciation = soup.select("#middlediv > div:nth-of-type(2)")[0].contents
        # 去掉不需要的.
        for appreciationtemp in originalappreciation[2 : len(originalappreciation) - 3]:
            appreciation += appreciationtemp.encode('utf-8')
        poem.content = content
        poem.tags = tags
        poem.appreciation = appreciation
        return None
            
    # 存入mongodb
    def persist(self):
        categories = self.get_categories()
        if not categories:
            print "年代为空，返回."
            return None
        for category in categories:
            print "正在处理: ", category
            authors = self.get_authors(category)
            if not authors:
                print "该年代作者为空，跳过该年代. categoryurl:", category.url
                continue
            for author in authors:
                print "正在处理 ", author
                poems = self.get_author_poems(category.name, author)
                if not poems:
                    print "该作者诗词为空或已存在，跳过该作者. authorurl:", author.url
                    continue
                for poem in poems:
                    print "正在处理:", poem
                    self.get_poem_content(category.name, author.name, poem)
                    # 不存在插入，存在更新poem列表.
                    existedpoems = DBQuery.authorpoems(category.name, author.name)
                    if existedpoems:
                        existedpoems.append(poem)
                        DBChange.updateauthorpoems(category.name, author.name, author.url, existedpoems)
                    else:
                        DBChange.persist(category, author, poem)
