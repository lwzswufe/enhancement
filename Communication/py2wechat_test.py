# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import itchat           # 需要用pip导入 itchat包
import datetime
import time
from itchat.content import *
import threading
import Communication.wechat_reply as wechat_reply


class send_message_to_wechat(object):
    def __init__(self):
        self.receiver = list()

    @itchat.msg_register(isGroupChat=False, msgType=TEXT)  # 个人私信
    def group_text_reply(msg):
        return wechat_reply.reply_signal(msg)

    @itchat.msg_register(isGroupChat=True, msgType=TEXT)   # 微信群
    def group_text_reply(msg):
        return wechat_reply.reply_group(msg)

# 自动登陆微信
    def wechat_login(self):
        itchat.auto_login()
        print('微信登陆成功')

    def get_receiver(self):
        return self.receiver

    def push_time(self):
        localtime = datetime.datetime.now()    # 获取当前时间
        now = localtime.strftime('%H:%M:%S')
        itchat.send(now, toUserName='filehelper')
        print(now)

    def push(self):
        itchat.send('Stock_WeChat 已开始执行！', toUserName='filehelper')
        print('Stock_WeChat 已开始执行！')
        while True:
            try:
                self.get_push()
                time.sleep(2.9)
            except KeyboardInterrupt:
                itchat.send('Stock_WeChat 已执行完毕！\n', toUserName='filehelper')
                print('Stock_WeChat 已执行完毕！\n')
                break

    def remind(self):
        itchat.send('Stock_WeChat 已开始执行！', toUserName='filehelper')
        print('Stock_WeChat 已开始执行！')
        while True:
            try:
                self.push_time()
                time.sleep(2.9)
            except KeyboardInterrupt:
                itchat.send('Stock_WeChat 已执行完毕！\n',
                            toUserName='filehelper')
                print('Stock_WeChat 已执行完毕！\n')
                break


class trade_list(object):
    def __init__(self, fname='test'):
        self.code = list()
        self.time = list()
        self.price = list()
        self.name = list()
        self.context = list()
        self.textname = fname

    def append(self, code, name, time_str, price, repet=False, buyorsell='买入'):
        if repet or code not in self.code:
            self.code.append(code)
            self.name.append(name)
            self.time.append(time_str)
            self.price.append(price)
            context = buyorsell + ' ' + code + ' ' + name + ' 价格 ' +\
                      str(price) + '\n'
            self.context.append(context)

    def write(self):
        PC = file_address()
        fname = PC + self.textname
        if len(self.context) > 0:
            f = open(fname, 'w')
            line = '时间 ' + self.time[-1] + '\n'
            f.write(line)
            for line in self.context:
                f.write(line)
                print(line)
            f.close()

    def get_data(self):
        write_df = pd.DataFrame({'code': self.code, 'name': self.name,
                                 'time': self.time, 'price': self.price})
        return write_df

    def update(self, code, name=False, time=False, price=False):
        if code not in self.code:
            return
        i = self.code.index(code)
        if time:
            self.time[i] = time
        if price:
            self.price[i] = price
        if name:
            self.name[i] = name


def file_address():
    PC = 'D:\\Share\\Trade\\'
    return PC


if __name__ == '__main__':
    sw = send_message_to_wechat()
    sw.wechat_login()                                       # 扫描二维码并登陆
    th_1 = threading.Thread(target=itchat.run)
    th_2 = threading.Thread(target=sw.remind)
    th_1.start()
    th_2.start()
    print('start over')

