#! /bin/bash
### Deprecated.   功能已由 gen_gzh_urls.py 替代.

# 从公众号列表页面中获取每篇文章的链接.
sed -n '/weui_media_title.*weixin/p' 图解金融.txt | sed -n '/删除/!p' | sed -n 's/<h4 class="weui_media_title" hrefs="\(.*\)">/\1/p' > 图解金融_url.txt
