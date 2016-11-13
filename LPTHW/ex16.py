#coding:utf-8
from sys import argv

script, filename = argv

print "We're going to erase %r." % filename
print "If you don't want that, hit CTRL-C (^C)."
print "If you do want that, hit RETURN."

# CTRL-C 可以直接退出 raw_input()
raw_input("?")

print "Opening the file..."
target = open(filename, 'w')              # 先open()

print "Truncating the file.  Goodbye!"
target.truncate()                         # 再truncate()， 清空文件，文件还在。

print "Now I'm going to ask you for three lines."

line1 = raw_input("line 1: ")
line2 = raw_input("line 2: ")
line3 = raw_input("line 3: ")

print "I'm going to write these to the file."

target.write(line1)                       # 在 write() 写入内容到文件里.
target.write("\n")
target.write(line2)
target.write("\n")
target.write(line3)
target.write("\n")

print "And finally, we close it."
target.close()                            # 最后close()掉.
