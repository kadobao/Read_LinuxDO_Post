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