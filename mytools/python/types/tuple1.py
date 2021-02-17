# tuple 元组
import collections


def test1():
    lax_coordinates = (33.9425, -118.408056)
    # 元组拆包.  平行赋值方式. 把可迭代对象里元素，一并赋值到变量组成的元组中.
    city, year, pop, chg, area = ('Tokyo', 2003, 32450, 0.66, 8014)
    # 元组拆包.
    latitude, longitude = lax_coordinates
    # [], (), {} 里的换行会被忽略.  可以不用写 \
    traveler_ids = [('USA', '31195855'), ('BRA', 'CE342567'),
                    ('ESP', 'XDA205856')]

    # % 能被匹配到对应的元组上, 同样属于元组拆包.
    for passport in sorted(traveler_ids):
        print('%s/%s' % passport)
    # for 循环提取元组中的元素,  第二个元素没有用到, 赋值给"_"占位符.
    for country, _ in traveler_ids:
        print(country)

    # 利用拆包，不使用中间变量交换变量值.
    a = 3
    b = 4
    a, b = b, a
    print(a)
    print(b)


# 元组拆包: *
def test2():
    print("=====test2=====")
    print(divmod(20, 8))

    # * 可以将可迭代对象拆成多个作为函数参数, 这里不加*, 报错: TypeError: divmod expected 2 arguments, got 1
    t = (20, 8)
    print(divmod(*t))

    # * 可以用来接收剩下的元素.
    a, b, *rest = range(10)
    print("a: ", a, "b: ", b, "rest: ", rest)
    # *var 可以在任意位置.
    a, b, *body, c = range(10)
    print("a: ", a, "b: ", b, "body: ", body, "c: ", c)


# 嵌套元组拆包.
def test3():
    print("=====test3=====")

    metro_areas = [
        ('Tokyo', 'JP', 36.933, (35.687922, 139.691667)),
        ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
        ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
        ('New York', 'US', 20.104, (40.808611, -74.020386)),
        ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833))
    ]
    print('{:15} | {:^9} | {:^9}'.format('', 'lat.', 'long.'))
    fmt = '{:15} | {:^9.4f} | {:^9.4f}'
    for name, cc, pop, (latitude, longitude) in metro_areas:
        if (longitude <= 0):
            print(fmt.format(name, latitude, longitude))


# 具名元组
def test4():
    print("=====test4=====")
    # 空格分隔开的字段名.
    City = collections.namedtuple('City', 'name country population coordinates')
    tokyo = City('Tokey', 'JP', 36.933, (35.689722, 139.691667))
    print(tokyo)
    print(tokyo.population, tokyo.coordinates)

    # 等价于上面. 字符串组成的可迭代对象.
    City2 = collections.namedtuple('City2', ['name', 'country', 'population', 'coordinates'])
    tokyo2 = City2('Tokey', 'JP', 36.933, (35.689722, 139.691667))
    print(tokyo2)
    print(tokyo2.population, tokyo2.coordinates)

    # 元组的类属性
    print(City._fields)


test1()
test2()
test3()
test4()

test1()
test2()
test3()
test4()
