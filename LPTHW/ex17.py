#coding:utf-8
from sys import argv
from os.path import exists

script, from_file, to_file = argv

print "Copying from %s to %s" % (from_file, to_file)

# we could do these two on one line too, how?
input = open(from_file)
indata = input.read()

print "The input file is %d bytes long" % len(indata)       # len() 计算字节数,非字符数.

print "Does the output file exist? %r" % exists(to_file)    # exists() 是否存在.
print "Ready, hit RETURN to continue, CTRL-C to abort."
raw_input()

output = open(to_file, 'w')       # 不存在，新建
output.write(indata)

print "Alright, all done."

output.close()
input.close()
