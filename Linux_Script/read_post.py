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