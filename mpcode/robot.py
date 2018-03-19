#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from werobot import WeRoBot

myrobot = WeRoBot()
myrobot.config.from_pyfile('config.py')

weapitoken = "yourapitoken"


def tagcheck(func):
    def wrapper(args):
        url4p = "https://yoururl/weapis/user/" + weapitoken
        url4g = url4p + '?uid=' + args.source
        r = requests.get(url4g).json()
        if (r['tag'] > 0):
            r['tag'] += 1
            r = requests.put(url4p, json = {'uid': args.source, 'count': r['count'], 'tag': r['tag']})
        else:
            return func(args)
    return wrapper


@myrobot.subscribe
def subscribe(message):
    url = "https://yoururl/weapis/user/" + weapitoken
    r = requests.post(url, json = {'uid': message.source})
    if (r.status_code == 200):
        return """前世的五百次回眸，才换得今生的一次擦肩而过。
Yunerself很庆幸和你相遇，希望以后都因为彼此而快乐！

请通过查看历史消息浏览往期推送，
或输入help了解公众号提供的服务。"""
    else:
        return "anythingyouwant"

@myrobot.unsubscribe
def unsubscribe(message):
    url = "https://yoururl/weapis/user/" + weapitoken
    r = requests.delete(url, json = {'uid': message.source})
    if (r.status_code == 200):
	    return True
    else:
	    return False

@tagcheck
def about(message):
    return """我是天空里的一片云，
偶尔投影在你的波心——
    你不必讶异，
    更无须欢喜——
在转瞬间消灭了踪影。"""

@tagcheck
def count(message):
    url4p = "https://yoururl/weapis/user/" + weapitoken
    url4g = url4p + '?uid=' + message.source
    r = requests.get(url4g).json()
    if (r['uid'] == 'null'):
        r = requests.post(url4p, json = {'uid': message.source}).json()
    return "你在Yunerself已留言%s次，有你的回应，我很幸福！" % r['count']

@tagcheck
def help(message):
    return """请输入以下关键字获得相关服务：
a/about - 关于公众号的简介
c/count - 统计你在公众号后台的留言次数
h/help - 帮助说明
m/magic - 一个随时可能变化的未知功能
o/over - 结束留言
w/wish - 开始留言
y/yunerself - 功能同帮助说明

输入关键字以外的任意内容，系统会随机返回一篇往期推送"""

@tagcheck
def magic(message):
    return "嘛咪嘛咪轰，我是河神，现在赶快对着屏幕喊出你的愿望"

@tagcheck
def wish(message):
    url4p = "https://yoururl/weapis/user/" + weapitoken
    url4g = url4p + '?uid=' + message.source
    r = requests.get(url4g)
    if (r.json()['uid'] == 'null'):
        r = requests.post(url4p, json = {'uid': message.source})
    r = requests.put(url4p, json = {'uid': message.source, 'count': r.json()['count'], 'tag': 1})
    if (r.status_code == 200):
        return "哇塞，你一定要多多留言哟～"
    else:
        return "anythingyouwant"

def over(message):
    url4p = "https://yoururl/weapis/user/" + weapitoken
    url4g = url4p + '?uid=' + message.source
    r = requests.get(url4g).json()
    if (r['uid'] == 'null' or r['tag'] == 0):
        return "淘气，还没有开始留言呢，就想着要结束啦"
    msg = "又被你调戏了，但是我愿意～"
    if (r['tag'] > 1):
        r['count'] += 1
	msg = "Yunerself已经收到你的留言啦，正在认真阅读呢，么么哒～"
    r = requests.put(url4p, json = {'uid': message.source, 'count': r['count'], 'tag': 0})
    if (r.status_code == 200):
        return msg
    else:
        return "anythingyouwant"

def article(message):
    url4p = "https://yoururl/weapis/user/" + weapitoken
    url4g = url4p + '?uid=' + message.source
    r = requests.get(url4g).json()
    if (r['tag'] == 0):
        url = "https://yoururl/weapis/article/" + weapitoken
        r = requests.get(url).json()
        if (r['title'] == 'null'):
            return "anythingyouwant"
        return [
            [
                r['title'],
                r['description'],
                r['img'],
                r['url']
            ]
        ]
    else:
        r['tag'] += 1
        r = requests.put(url4p, json = {'uid': message.source, 'count': r['count'], 'tag': r['tag']})

@myrobot.voice
def voicedispatch(message):
    keyword = message.recognition[:-1]
    if (keyword == u"简介"):
	    return about(message)
    elif (keyword == u"统计"):
	    return count(message)
    elif (keyword == u"帮助"):
	    return help(message)
    elif (keyword == u"魔法"):
	    return magic(message)
    elif (keyword == u"结束留言"):
	    return over(message)
    elif (keyword == u"我要留言"):
	    return wish(message)
    else:
	    return article(message)

myrobot.add_filter(func=about, rules=["A", "a", "about"])
myrobot.add_filter(func=count, rules=["C", "c", "count"])
myrobot.add_filter(func=help, rules=["H", "h", "help", "Y", "y", "yunerself"])
myrobot.add_filter(func=magic, rules=["M", "m", "magic"])
myrobot.add_filter(func=over, rules=["O", "o", "over"])
myrobot.add_filter(func=wish, rules=["W", "w", "wish"])
myrobot.add_filter(func=article, rules=[re.compile(u"[A-Za-z]|[0-9]|[\u0000-\uFFFF]")])