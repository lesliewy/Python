# -*- coding:utf-8 -*-

import urllib.request


# 获取指定url的文件, 保存至本地
def persist_file(url, full_file_path, encoding):
    try:
        # 构建请求的request
        request = urllib.request.Request(url)
        # 利用urlopen获取页面代码
        response = urllib.request.urlopen(request)
        # 将页面转换编码
        content = response.read().decode(encoding)

        # 保存至文件
        file_handle = open(full_file_path, 'w')
        file_handle.write(content)
        file_handle.close()
        return content
    except urllib.request.URLError as e:
        if hasattr(e, "reason"):
            print("连接失败,错误原因", e.reason)
            return None
