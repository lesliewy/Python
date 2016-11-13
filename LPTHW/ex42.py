#coding:utf-8
# class A(object)  object 必须加.
class TheThing(object):

    # 设置class中的变量, 第一个参数表示该class自己。通常用self表示.
    def __init__(self):
        self.number = 0

    def some_function(self):
        print "I got called."

    def add_me_up(self, more):
        self.number += more
        return self.number

# two different things
a = TheThing()
b = TheThing()

# 可以理解为add_me_up(a), 但是不可以这样写。
a.some_function()
b.some_function()

# 可以理解为add_me_up(a, 20), 但是不可以这样写。
print a.add_me_up(20)
print a.add_me_up(20)
print b.add_me_up(30)
print b.add_me_up(30)

# 调用方法自己的属性
print a.number
print b.number
