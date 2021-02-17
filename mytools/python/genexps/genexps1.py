# generator expression 生成器表达式.

# genexps: 使用 ()
# listcomps: 使用[]
#
# genexps 每次调用时取一个元素. 不会一次性生成多个.  大量数据时可以节省内存.
def test1():
    print("=====test1=====")
    symbols = "abcdefghi"
    print(tuple(ord(s) for s in symbols))

    import array
    print(array.array('I', (ord(c) for c in symbols)))

    colors = ['black', 'white']
    sizes = ['S', 'M', 'L']
    for tshirt in ((color, size) for color in colors for size in sizes):
        print(tshirt)

    for tshirt in ('%s %s' % (c, s) for c in colors for s in sizes):
        print(tshirt)


test1()
