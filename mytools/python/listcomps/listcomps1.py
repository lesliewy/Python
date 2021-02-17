# list comprehension 列表推导.
# 作用: 生成list.

# 使用listcomps通常原则: 只用来创建列表; 保持简短(不超过1行);
def test1():
    print("====test1====")
    symbols = "abcde"
    codes = []
    for symbol in symbols:
        codes.append(ord(symbol))
    print(codes)

    # 等价于上面.
    codes = [ord(s) for s in symbols]
    print(codes)

    print([s for s in symbols])


def test2():
    print("=====test2=====")
    symbols = "abcdefghijkl"
    codes = [ord(s) for s in symbols if ord(s) > 100]
    print(codes)
    print([s for s in symbols if ord(s) > 100])

    # filter  等价于上面, 不过显然listcomps可读性更高.
    print("filter:")
    print(list(filter(lambda c: c > 100, map(ord, symbols))))


def test3():
    print("======test3======")
    colors = ['black', 'white']
    sizes = ['S', 'M', 'L']
    # 笛卡尔积  元素是tuple的list.  注意，for顺序的变化导致tuple中顺序的变化.
    tshirts = [(color, size) for color in colors for size in sizes]
    print(tshirts)
    tshirts = [(color, size) for size in sizes for color in colors]
    print(tshirts)
    tshirts = [(size, color) for color in colors for size in sizes]
    print(tshirts)


test1()
test2()
test3()
