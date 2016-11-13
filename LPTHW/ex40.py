#coding:utf-8
# Python中的dict,  有点像java中的map
cities = {'CA': 'San Francisco', 'MI': 'Detroit',
                     'FL': 'Jacksonville'}

cities['NY'] = 'New York'
cities['OR'] = 'Portland'

def find_city(themap, state):
    # 判断key是否存在.
    if state in themap:
        return themap[state]
    else:
        return "Not found."

# ok pay attention!   dict 中都可以放函数
cities['_find'] = find_city

while True:
    print "State? (ENTER to quit)",
    state = raw_input("> ")

    # 这种写法也可以
    if not state: break

    # this line is the most important ever! study!    使用dict中的函数
    city_found = cities['_find'](cities, state)
    print city_found

# dict 中可以存放任何类型，
mymap = {'a': 'A', 'b': 'B', 1: 11, 'c': 3}
print mymap['a']
# 数字1不表示第一个,而表示key为1.
print mymap[1]
print mymap['c']
