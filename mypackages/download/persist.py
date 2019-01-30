# -*- coding:utf-8 -*-

import os
import urllib.request

from files import file_util


# 获取指定url的文件, 保存至本地
def persist_file(url, full_file_path, encoding="utf8", withUserAgent=False, headers=None, method='GET'):
    try:
        # 构建请求的request
        request = urllib.request.Request(url, method=method)

        # 某些网站禁止爬虫，需要模拟浏览器访问.
        if (withUserAgent):
            request.add_header('User-Agent',
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')

        if (headers):
            for (name, value) in headers.items():
                request.add_header(name, value);

        # 利用urlopen获取页面代码
        response = urllib.request.urlopen(request)
        # 将页面转换编码
        content = response.read().decode(encoding)

        # 保存至文件
        file_util.write_file(content, full_file_path, 'w')
        '''
        file_handle = open(full_file_path, 'w')
        file_handle.write(content)
        file_handle.close()
        '''
        return content
    except urllib.request.URLError as e:
        print("连接失败,url:", url, " 错误原因", e)
        return None
        '''
        if hasattr(e, "reason"):
            print("连接失败,错误原因", e.reason)
            return None
        '''


#####
#
# 下载文件.
#
#####
def persis_file_times(url, full_file_path, file_size=0):
    if (not os.path.isfile(full_file_path) or (file_size > 0 and os.path.getsize(full_file_path) <= file_size)):
        max_times = 3;
        while (max_times > 0):
            max_times -= 1;
            if (os.path.isfile(full_file_path) and os.path.getsize(full_file_path) > file_size):
                break;
            persist_file(url, full_file_path);
    return os.path.isfile(full_file_path) and os.path.getsize(full_file_path) > file_size;


# 获取指定url的内容.
def get_response(url, method='GET', data=None, encoding="utf8", withUserAgent=False, headers=None):
    try:
        # 构建请求的request
        request = urllib.request.Request(url, data=data, headers=headers, method=method)

        # 某些网站禁止爬虫，需要模拟浏览器访问.
        if (withUserAgent):
            request.add_header('User-Agent',
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
        '''
        if (headers):
            for (name, value) in headers.items():
                request.add_header(name, value);
        '''

        # 利用urlopen获取页面代码
        response = urllib.request.urlopen(request)
        # 将页面转换编码
        content = response.read().decode(encoding)
        return content
    except urllib.request.URLError as e:
        print("连接失败,url:", url, " 错误原因", e)
        return None
