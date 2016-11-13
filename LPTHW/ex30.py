#coding:utf-8
people = 30
cars = 40
buses = 15


# 使用的elif
if cars > people:
    print "We should take the cars."
elif cars < people:
    print "We should not take the cars."
else:
    print "We can't decide."

if buses > cars:
    print "That's too many buses."
elif buses < cars:
    print "Maybe we could take the buses."
else:
    print "We still can't decide."

if people > buses:
    print "Alright, let's just take the buses."
else:
    print "Fine, let's stay home then."

# 显然， elif 后面可以没有最后那个 else
if 5 < 3:
    print "leslie: 5 < 3"
elif 5 > 3:
    print "leslie 5 > 3"
