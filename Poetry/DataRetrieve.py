# -*- coding:utf-8 -*-
import urllib
import urllib2
import string
import re
import time
import socket
# from import 方式引入的，使用时可以省略module名
from bs4 import BeautifulSoup
from bs4 import NavigableString
from Category import *
from Author import *
from Poem import *
from DBQuery import *
from DBChange import *

"""
 解析诗词名句网(http://www.shicimingju.com/)的信息, 并存入mongodb
"""
class DataShicimingju:
    def __init__(self):
        self.URL = "http://www.shicimingju.com"
        self.timeout = 7

    # 获取年代. http://www.shicimingju.com/左侧的年代诗人.
    # 返回值形式 {"先秦":"/category/xianqinshiren"}
    def get_categories(self):
        try:
            # 构建请求的request
            request = urllib2.Request(self.URL)
            # 利用urlopen获取页面代码
            response = urllib2.urlopen(request, timeout = self.timeout)
            # 将页面转化为UTF-8编码
            agepage = response.read().decode('utf-8')
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
            category.name = catename.encode('utf-8')
            category.url = cateurl
            categories.append(category)
        return categories
        
    # 获取年代内的诗人. http://www.shicimingju.com/category/xianqinshiren
    def get_authors(self, category):
        categoryurl = category.url
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
            authorname = atag[0].contents[0].encode('utf-8')
            authorurl = atag[0]["href"]
            # 隋朝最后两位作者有问题，跳过
            #if len(atag[0].contents) < 2:
            #    continue
            # 最后需要去掉前后()
            numofpoems = string.atoi(atag[0].contents[1].string[1:-1])
            author = Author()
            author.name = authorname
            # 隋朝最后两位作者有问题，跳过
            #if author.name == "佚名":
            #    continue
            author.url = authorurl
            author.numofpoems = numofpoems
            authors.append(author)
        return authors

    # 获取某个作者的所有诗列表.
    def get_author_poems(self, categoryname, author):
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
            if(i > 1):
                fullauthorurl = re.sub(re.compile("(_\d*)?\.html"), "_" + str(i) + ".html", fullauthorurl)

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
                    allbrief = brieftext[0].encode('utf-8')
                    pattern = re.compile('.*?<img.*?>(.*?)</div>', re.S)        
                    matchobj = re.search(pattern, allbrief)
                    # 有的简介里有作者图片.
                    if matchobj:
                        brief = matchobj.group(1).strip()
                        author.brief = brief
                    # 不存在图片.
                    else:
                        brief = brieftext[0].contents[0].encode('utf-8')
                print "brief:", brief
            # 诗列表 #chaxun_miao > div.shicilist > ul:nth-child(1)
            allpoemtext = soup.select("#chaxun_miao > div.shicilist > ul")
            if not allpoemtext:
                print "没有诗存在，返回"
                return allpoems
            for poemul in allpoemtext:
                poem = Poem()
                line1 = poemul.select("> li:nth-of-type(1) > a")
                poem.url = line1[0]["href"]
                poem.name = line1[0].string.encode('utf-8')
                allpoems.append(poem)
        return allpoems

    # 获取诗词正文.
    def get_poem_content(self, categoryname, authorname, poem):
        poemname = poem.name
        poemurl = poem.url
        # 查询是否已经存在
        existednum = DBQuery.authorpoemcount(categoryname, authorname, poemname, poemurl)
        if(existednum > 0):
            print "已存在", authorname, "的", poemname
            return False

        fullpoemurl = self.URL + poemurl
        trynum = 0
        while trynum <= 9:
            trynum += 1
            try:
                request = urllib2.Request(fullpoemurl)
                response = urllib2.urlopen(request, timeout = self.timeout)
                poempage = response.read().decode('utf-8')
                if not poempage:
                    print u"获取诗正文页面出错."
            except urllib2.URLError, e:
                if hasattr(e, "reason"):
                    print u"获取诗正文失败:",  fullpoemurl, " 错误原因", e.reason
                    return False
            except socket.error:
                response.close()
                response = None
                time.sleep(15)
                print trynum, "次timeout"
                continue
            else:
                break
        soup = BeautifulSoup(poempage)
        # 诗词内容 #shicineirong
        originalcontent = soup.select("#shicineirong")[0].contents
        # test begin
        #originalcontent = soup.select("#shicineirong > div.para")[0].contents
        # test end
        content = ""
        for contenttemp in originalcontent:
            # navigatablestring 需要先encode.
            content += contenttemp.encode('utf-8')
        # 分类标签 #middlediv > div.zhuti.yuanjiao > div.listscmk > a:nth-child(1)
        tags = []
        tagstext = soup.select("#middlediv > div.zhuti.yuanjiao > div.listscmk > a")
        # test begin
        #tagstext = soup.select("#shicineirong > div.listscmk > a")
        # test end
        if tagstext:
            for tag in tagstext:
                tags.append(tag.string)
        # 赏析 #middlediv > div:nth-child(2)
        appreciation = ""
        originalappreciation = soup.select("#middlediv > div:nth-of-type(2)")[0].contents
        # test begin
        #originalappreciation = soup.select("#middlediv > div > div:nth-of-type(3)")[0].contents
        # test end
        # 去掉不需要的.
        tailindex = len(originalappreciation) - 2
        str1 = originalappreciation[len(originalappreciation) - 3]
        if (isinstance(str1, NavigableString) and str1.startswith('[url=http')):
            tailindex = len(originalappreciation) - 3

        for appreciationtemp in originalappreciation[2 : tailindex]:
            appreciation += appreciationtemp.encode('utf-8')
        poem.content = content
        poem.tags = tags
        poem.appreciation = appreciation
        return True
            
    # 存入mongodb
    def persist(self):
        categories = self.get_categories()
        if not categories:
            print "年代为空，返回."
            return None
        for category in categories:
            if category.name in ["先秦", "汉朝", "魏晋", "南北朝", "隋朝"]:
                print category.name, "处理完了, 跳过."
                continue
            print "正在处理: ", category
            authors = self.get_authors(category)
            if not authors:
                print "该年代作者为空，跳过该年代. categoryurl:", category.url
                continue
            i = 0
            for author in authors:
                i += 1
                if author.name in ["白居易", "杜甫", "李白", "齐己", "刘禹锡", "徐铉", "元稹", "韦应物", \
                "李商隐", "贯休", "杜牧", "刘长卿", "陆龟蒙", "皎然", "罗隐", "姚合", "许浑"]:
                    print author.name, "处理完了, 跳过."
                    continue
                print "author ", i, " 正在处理 ", author
                poems = self.get_author_poems(category.name, author)
                if not poems:
                    print "该作者诗词为空或已存在，跳过该作者. authorurl:", author.url
                    continue
                j = 0
                for poem in poems:
                    j += 1

                    print "poem", j, "/", author.numofpoems,  "正在处理:", poem
                    if not self.get_poem_content(category.name, author.name, poem):
                        continue
                    # 不存在插入，存在更新poem列表.
                    existedpoemscursor = DBQuery.authorpoems(category.name, author.name, author.url)
                    if (existedpoemscursor and existedpoemscursor.count() > 0):
                        DBChange.updateauthorpoems(category.name, author.name, author.url, poem)
                    else:
                        DBChange.persist(category, author, poem)

                    #test begin
                    #if poem.name == '行路难 其二':
                    #    return;
                    #test end
