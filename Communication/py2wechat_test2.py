# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import itchat
from itchat.content import *


@itchat.msg_register(TEXT, isGroupChat=True)
def group_text_reply(msg):
    if u'关闭' in msg['Text']:
        return u'已关闭'
    elif u'开启' in msg['Text']:
        return u'已经在运行'
    return u'输入"关闭"或者"开启"测试功能'


@itchat.msg_register(TEXT, isGroupChat=True)
def group_text_reply(msg):
    if u'开启' in msg['Text']:
        replyToGroupChat = True
        return u'重新开启成功'


if __name__ == "__main__":
    pass