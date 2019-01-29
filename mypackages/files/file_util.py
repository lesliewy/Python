# coding:utf-8
import os
import shutil
import re
import numpy


# 创建目录.
def create_dir(fullpath):
    is_exists = os.path.exists(fullpath)
    if not is_exists:
        os.makedirs(fullpath)


# 删除目录
def delete_dir(dir_path):
    # os.remove(dir_path) 删除文件, os.removedirs(dir_path) 删除空目录.
    shutil.rmtree(dir_path)


# 读文件
def read_file(file_path):
    with open(file_path) as f:
        content = f.read()
    return content


# 写文件
def write_file(str, file_path, mode):
    with open(file_path, mode) as fw:
        fw.write(str)


def write_lines(obj, file_path, mode):
    with open(file_path, mode) as fw:
        if isinstance(obj, (str)):
            # fw.write('%s' % '\n'.join(result))
            fw.writelines(obj)
        elif isinstance(obj, (list)):
            numpy.savetxt(file_path, numpy.array(obj), fmt="%s")


# 递归遍历文件, 获取指定父目录正则、文件名正则的所有文件名. 父目录是最终文件的父目录.
def get_files(dir, parent_name_reg=None, file_name_reg=None):
    for parent, dirnames, filenames in os.walk(dir):
        parent_dir_name = parent.split("/")[-1]
        result = []
        for filename in filenames:
            if parent_name_reg and not re.match(parent_name_reg, parent_dir_name):
                continue
            if file_name_reg and not re.match(file_name_reg, filename):
                continue
            result.append(os.path.join(parent, filename))
        for dirname in dirnames:
            dir_result = get_files(os.path.join(parent, dirname), parent_name_reg=parent_name_reg,
                                   file_name_reg=file_name_reg)
            if dir_result:
                result.extend(dir_result)
        return result;


# print(get_files("/Users/leslie/MyProjects/Data/temp"))
