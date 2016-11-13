#coding:utf-8
x = "There are %d types of people." % 10                     # x 就是一个str.
binary = "binary"
do_not = "don't"
y = "Those who know %s and those who %s." % (binary, do_not) # y 就是一个str.

print x
print y

print "I said: %r." % x               #  %r 不用考虑是number 还是str 还是bool，都可以用. 如果是str, 相当于'%s'
print "I also said: '%s'." % y

hilarious = False
joke_evaluation = "Isn't that joke so funny?! %r"

print joke_evaluation % hilarious          # hilarious 没有''

w = "This is the left side of..."
e = "a string with a right side."

print w + e       # 可以用 + 连接.
