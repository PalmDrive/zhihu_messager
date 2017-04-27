# coding=utf-8
import os
import sys
import time
from zhihu_oauth import *

# 使用命令行：python3 main.py 1 0
# 多进程则：
#   python3 main.py 3 0
#   python3 main.py 3 1
#   python3 main.py 3 2


# 处理登陆token，如果未登录，则提示，登陆后保存登陆凭证
TOKEN_FILE = 'token.pkl'
client = ZhihuClient()
if os.path.isfile(TOKEN_FILE):
    client.load_token(TOKEN_FILE)
else:
    client.login_in_terminal()
    client.save_token(TOKEN_FILE)

msgs = [
    '''您好，打扰您1分钟的时间。 

我们是一支成立于斯坦福的团队，目前做了一款职业相关的高质量内容推荐APP，邀请您体验。 

在APP里输入你的行业、领域以及职位，就能收到工作息息相关、读完后不感觉浪费时间的文章。 

下载链接： http://ainterest-service-production.ailingual.cn/app-download?v=1（蹦出小窗口后点击顶部字母的链接）
Or 
APP store搜索：职得看
''',
    '''您好，打扰您1分钟的时间。 

我们是一支成立于斯坦福的团队，目前做了一款围绕职业的高质量内容推荐APP，邀请您体验这款产品，并希望能给我们一些建议。 

APP可以： 
1.根据您所在的行业、领域、职业，个性化推送高质量的文章（高质量版的今日头条） 
2.专题化的全面性阅读，比如：你想要了解“关于知乎的讨论与分析”，app会为你精选出全网关于这个话题的高质量文章

下载链接： http://ainterest-service-production.ailingual.cn/app-download?v=2（蹦出小窗口后点击顶部字母的链接）
Or 
APP store搜索：职得看
''',
    '''您好，打扰您1分钟的时间。

一年前，30多位年轻人挤在旧金山一个狭小的房间里向Guy Kawasaki请教1984年的商业智慧，于是做出了一款app，邀请您体验。

下载链接： http://ainterest-service-production.ailingual.cn/app-download?v=3（蹦出小窗口后点击顶部字母的链接）
Or 
APP store搜索：职得看

---------
Guy Kawasaki：1984年在苹果担任长达4年的首席布道者（Chief Evangelist），而最为人熟悉的就是那支苹果公司迄今为止最伟大的广告：一位白色t恤的女模特挥动铁锤砸烂电影屏幕，由此开启了个人电脑的全新时代。
''',
    '''您好，

我们是一支成立于斯坦福的团队，设计了一款个性化内容推荐APP，将

- 36kr、虎嗅、新芽、创业邦等超过30个科技平台的专栏作者
- 知乎里上千名优秀答主
- 订阅号里上万个作者

这些有着深刻洞察力的内容创作者的文章汇集在一起。

欢迎您体验～

下载链接： http://ainterest-service-production.ailingual.cn/app-download?v=4（蹦出小窗口后点击顶部字母的链接）
Or 
APP store搜索：职得看
''',
]

count = 0  # 关注者的第几个
cur = 0  # 当前消息编号
last = 0  # 上一次发到哪
allocTotal = int(sys.argv[1])   # 多进程发送，总进程数
allocated = int(sys.argv[2])    # 多进程发送，第几个进程

me = client.me()
print('process: ', allocated, ' start')


def send(p):
    global count, cur
    print('sending msg to:', p.id, p.name, ' count: ', count, ' cur: ', cur)
    cur = (cur+1) % len(msgs)
    r = me.message(p, p.name + msgs[cur])
    print('return: ', r)
    if not r[0] and r[1].find('对方没有关注你') < 0:  # 部分用户需要关注后才能发送
        return False
    count = count + 1
    time.sleep(20)
    return True

question = client.question(28754163)
for f in question.followers:
    if f.id == 0 or f.name == '匿名用户':   #部分用户匿名，不能发送
        continue
    if count < last or count % allocTotal != allocated:   # 多进程下，跳过不属于自己的部分
        count += 1
        continue
    try:
        if not send(f):   # 如果出错，则退出，可能的错误包括账号异常等
            break
    except Exception as inst:   # 其他网络错误，一概忽略
        print('catch error: ', inst)
        time.sleep(20)
