#coding:utf-8
#  -- coding: utf-8 --   有中文时必须加 coding,  coding前不能有代码、空行，但可以有注释.
my_name = 'Zed A. Shaw'
my_age = 35 # not a lie
my_height = 74 # inches
my_weight = 180 # lbs
my_eyes = 'Blue'
my_teeth = 'White'
my_hair = 'Brown'

print "Let's talk about %s." %my_name    # 中间没有 ,
print "He's %d inches tall." % my_height
print "He's %d pounds heavy." % my_weight
print "Actually that's not too heavy."
print "He's got %s eyes and %s hair." % (my_eyes, my_hair)    # 多个用 %(var1, var2)
print "His teeth are usually %s depending on the coffee." % my_teeth

# this line is tricky, try to get it exactly right
print "If I add %d, %d, and %d I get %d." % (
          my_age, my_height, my_weight, my_age + my_height + my_weight)


print "leslie %s" %my_age         # 没有报错.
#print "leslie %d" %my_eyes       # 报错，不能将 str 转换为number
