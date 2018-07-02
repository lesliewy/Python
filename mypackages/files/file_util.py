# coding:utf-8
import os
import shutil


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

def write_lines(str, file_path, mode):
    with open(file_path, mode) as fw:
        # fw.write('%s' % '\n'.join(result))
        fw.writelines(str)
