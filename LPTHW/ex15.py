#coding:utf-8
from sys import argv

script, filename = argv

txt = open(filename)                    # open() 操作文件。

print "Here's your file %r:" % filename
print txt.read()          # read() 获取文件内容.

print "Type the filename again:"
file_again = raw_input("> ")

txt_again = open(file_again)

print txt_again.read()
