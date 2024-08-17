# 文件夹结构

├── Linux_Script/
│   ├── __init__.py
│   ├── find_navigate_links.py
│   └── read_post.py
├── test.py


====================== 阅读LinuxDO帖子\test.py ======================
## 阅读LinuxDO帖子\test.py
```py
# test.py

from DrissionPage import ChromiumPage, ChromiumOptions
from time import sleep, time
from DrissionPage import WebPage
import random
from DrissionPage.errors import *

from Linux_Script import read_post, find_navigate_links

# 创建一个配置对象，并设置自动分配端口
co = ChromiumOptions()

# 使用配置对象创建一个 ChromiumPage 对象
page = WebPage(chromium_options=co)

page.set.window.max()

# 打开目标网页
page.get('https://linux.do/u/momo4/activity/topics')

# 初始化帖子计数器
post_count = 0

# 初始化 numerator 列表
numerator_list = []

# 记录滚动开始的时间
start_time = time()

while True:
    # 生成一个随机数用于滚动像素
    scroll_distance = random.randint(240, 300)
    page.scroll.down(scroll_distance)
    page.wait(1)

    # 获取文档的高度
    document_height = page.run_js('return document.documentElement.scrollHeight;')
    # 获取视口的高度
    viewport_height = page.run_js('return window.innerHeight;')
    # 获取当前滚动条的位置
    scroll_position = page.run_js('return window.scrollY || window.pageYOffset || document.body.scrollTop + (document.documentElement.scrollTop || 0);')

    # 计算差值
    difference = document_height - (scroll_position + viewport_height)

    # 记录滚动结束的时间
    end_time = time()
    elapsed_time = end_time - start_time

    # 判断是否滚动到底部
    if difference <= 0:
        print(f'文档的高度: {document_height}, 视口的高度: {viewport_height}, 当前滚动条的位置: {scroll_position}, 到达页面底部, 差值: {difference}')

        personal_link = find_navigate_links.find_navigate_links(page)
        print(f'找到的链接数量: {personal_link[0]}')
        print(f'链接列表: {personal_link[1]}')
        for i, link in enumerate(personal_link[1]):
            post_count, numerator_list = read_post.read_post(page, link, i, post_count, numerator_list)
        break
    elif elapsed_time > 2:
        print(f'文档的高度: {document_height}, 视口的高度: {viewport_height}, 当前滚动条的位置: {scroll_position}, 到达页面底部, 差值: {difference}')

        personal_link = find_navigate_links.find_navigate_links(page)
        print(f'找到的链接数量: {personal_link[0]}')
        print(f'链接列表: {personal_link[1]}')
        for i, link in enumerate(personal_link[1]):
            post_count, numerator_list = read_post.read_post(page, link, i, post_count, numerator_list)
        break
    elif elapsed_time > 100000:
        pass
    else:
        print(f'文档的高度: {document_height}, 视口的高度: {viewport_height}, 当前滚动条的位置: {scroll_position}, 未到达底部, 差值: {difference}')
```

====================== 阅读LinuxDO帖子\Linux_Script\find_navigate_links.py ======================
## 阅读LinuxDO帖子\Linux_Script\find_navigate_links.py
```py
# Linux_Script/find_navigate_links.py

def find_navigate_links(page):
    eles = page.eles('css:a[href][class="title raw-link raw-topic-link"]')               
    links = eles.get.links()

    return len(links), links
```

====================== 阅读LinuxDO帖子\Linux_Script\read_post.py ======================
## 阅读LinuxDO帖子\Linux_Script\read_post.py
```py
# Linux_Script/read_post.py

import random
from DrissionPage.errors import *

def read_post(page, link, index, post_count, numerator_list):
    page.get(link)
    while True:
        # 生成一个随机数用于滚动像素
        scroll_distance = random.randint(240, 300)
        page.scroll.down(scroll_distance)
        page.wait(1)
        
        # 获取页面的总帖子数，因为发现了无回复的帖子，显示是0，而不是1 / 1，所以可以使用ElementNotFoundError解决这个问题
        post_num = page.ele("css:.timeline-replies", timeout=5)
        try:
            post_num = post_num.text
            print(post_num)
        
            # 解析分子和分母
            parts = post_num.split(' / ')

            numerator = int(parts[0])
            denominator = int(parts[1])
            
            # 检查分子和分母是否相同
            if numerator == denominator:
                # 再滑动3次
                for _ in range(3):
                    page.scroll.down(scroll_distance)
                print(f"这是第 {index} 次循环跳转，将跳转到 {link}")
                # 增加帖子计数器
                post_count += numerator
                break
            else:
                # 这个部分就是为了出来网站没有反应过来刷新，更新帖子的阅读情况的
                if denominator < 5:
                    numerator_list.append(numerator)
                    if 1 == denominator - numerator and numerator_list.count(numerator) >= 7:  
                        # 检查列表中相同值的次数
                        print("已经阅读完了这个话题，但网站没有反应过来")
                        print(f"这是第 {index} 次循环跳转，将跳转到 {link}")
                        # 增加帖子计数器
                        post_count += numerator
                        break
                else:
                    numerator_list.append(numerator)
                    if 5 > denominator - numerator and numerator_list.count(numerator) >= 7:  
                        # 检查列表中相同值的次数
                        print("已经阅读完了这个话题，但网站没有反应过来")
                        print(f"这是第 {index} 次循环跳转，将跳转到 {link}")
                        # 增加帖子计数器
                        post_count += numerator
                        break
        except ElementNotFoundError:
            print("找不到元素")
            break
    return post_count, numerator_list  # 返回更新后的 post_count 和 numerator_list
```

====================== 阅读LinuxDO帖子\Linux_Script\__init__.py ======================
## 阅读LinuxDO帖子\Linux_Script\__init__.py
```py
# Linux_Script/__init__.py

# 可以在这里导入包中的模块，以便用户可以直接从包中导入这些模块
from . import read_post
from . import find_navigate_links
```

