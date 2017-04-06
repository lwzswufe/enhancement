# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import itchat           # 需要用pip导入 itchat包
import datetime
import time
import json
import os
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Get_Trade_Day.get_trade_day import next_tradeday


class send_message_to_wechat(object):
    def __init__(self, time_interval=2.9,
                 msg_num_file='D:\\Python_Config\\WeChat_msg_num.json',
                 config_file='D:\\Python_Config\\WeChat_Send.json',
                 ):
        config = json.load(open(config_file, 'r', encoding="utf-8"))
        self.time_interval = time_interval
        self.next_reset_time = 0.0
        self.is_test = config['is_test']
        self.email_title = config['email_title']
        self.wechat_message_maxlen = config['wechat_message_maxlen']
        if self.is_test:
            self.wechat_receiver = [["filehelper"], []]
            self.email_receiver = [['3285670383@qq.com'], []]
        else:
            self.wechat_receiver = config['wechat_receiver']
            self.email_receiver = config['email_receiver']
        self.file_name = list()
        self.file_update_time = list()
        self.msg_send_num = list()
        self.is_change = list()
        self.file_exist = list()
        self.message_summary = ""
        self.wechat_message_list = list()
        self.send_email = send_email()

        for i, fn_list in enumerate(config['file_name']):
            self.is_change.append(0)
            self.file_name.append(dict())
            self.file_update_time.append(dict())
            self.file_exist.append(dict())
            self.msg_send_num.append(dict())
            for key_name in fn_list:
                fn = fn_list[key_name]
                if os.path.exists(fn):
                    self.file_exist[i][key_name] = True
                else:
                    self.file_exist[i][key_name] = False
                    print(fn, 'is not exist\n')
                self.file_name[i][key_name] = fn
                self.file_update_time[i][key_name] = 0    # 文件修改时间初始化
                self.msg_send_num[i][key_name] = 0        # 信息发送条数初始化

        print('initial over')
        self.msg_send_num = self.daily_reset()

    def message_add(self, context):                     # 汇总信息
        if len(self.message_summary) == 0:
            self.wechat_message_list.append("")
        self.message_summary += context
        flag = len(self.wechat_message_list) - 1
        if len(context) + len(self.wechat_message_list[flag]) < self.wechat_message_maxlen:
            self.wechat_message_list[flag] += context
        else:
            self.wechat_message_list.append(context)

    def daily_reset(self, reset_file='D:\\Python_Config\\WeChat_Send_reset.json'):
        fp = open(reset_file, 'r')
        reset_config = json.load(fp)
        fp.close()
        self.next_reset_time = reset_config['next_reset_time']
        if self.next_reset_time < time.time():
            time_stamp = next_tradeday(time_type='time_stamp')
            self.next_reset_time = time_stamp + 86400 - np.mod(time_stamp - 28800, 86400)  # 北京时间下午4点重置
            reset_config['next_reset_time'] = self.next_reset_time
            reset_config['time_str'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.next_reset_time))
            fp = open(reset_file, 'w')
            fp.write(json.dumps(reset_config))                                      # 重置文件//写入
            fp.close()
            for i, fn_list in enumerate(self.file_name):                            # 重置文件
                for fn in fn_list:
                    fp = open(fn_list[fn], 'w')
                    fp.close()
                    self.msg_send_num[i][fn] = 0
            reset_config['msg_send_num'] = self.msg_send_num
            print('reset over')
        else:
            self.msg_send_num = reset_config['msg_send_num']                        # 载入缓存
            print('no reset')
        print('next reset time:  ' + reset_config['time_str'])
        return reset_config['msg_send_num']

    def wechat_login(self):                        # 自动登陆微信
        if self.is_test:
            print(u'本地测试开启')
            itchat.auto_login()
        else:
            itchat.auto_login()
            print(u'微信登陆成功')

    def send_message(self, receiver_class=1):                      # 读取本地文件信息
        self.is_change[receiver_class] = 0                           # 标记是否变动
        for key_name in self.file_name[receiver_class]:
            if not self.file_exist[receiver_class][key_name]:        # 判断文件是否存在
                continue
            fn = self.file_name[receiver_class][key_name]
            update_time = os.stat(fn).st_mtime
            if self.file_update_time[receiver_class][key_name] < update_time:
                self.is_change[receiver_class] = 1
                f = open(fn, 'r')
                contexts = f.readlines()
                self.file_update_time[receiver_class][key_name] = update_time
                st = self.msg_send_num[receiver_class][key_name]
                for context in contexts[st:]:                             # 跳过已经推送的信息
                    self.message_add(context)
                    self.msg_send_num[receiver_class][key_name] += 1       # 记录信息条数
                f.close()

        self.wechat_push(receiver_class)                                   # 推送信息
        self.email_push(receiver_class)

    def cache_write(self, reset_file='D:\\Python_Config\\WeChat_Send_reset.json'):
        if sum(self.is_change) > 0:
            fp = open(reset_file, 'r')
            reset_config = json.load(fp)
            reset_config['msg_send_num'] = self.msg_send_num
            fp.close()

            fp = open(reset_file, 'w')
            fp.write(json.dumps(reset_config))                              # 重置文件//写入
            fp.close()

    def wechat_push(self, receiver_class=1):                              # 微信推送信息
        if self.is_test:
            print(self.wechat_message_list)
        else:
            for i, context in enumerate(self.wechat_message_list):
                for receiver in self.wechat_receiver[receiver_class]:
                    itchat.send(context, toUserName=receiver)
                time.sleep(2)

        self.wechat_message_list = list()

    def email_push(self, receiver_class):                      # 邮箱信息推送
        receivers = self.email_receiver[receiver_class]
        if len(receivers) == 0:
            print(self.message_summary)
        elif len(self.message_summary) > 0 and len(receivers) > 0:
            self.send_email.sends(receiver=receivers,
                                  context=self.message_summary,
                                  title=self.email_title[receiver_class])
        self.message_summary = ""

    def remind(self):                                          # 监控文件变化
        # self.wechat_push('Python_WeChat 已开始执行!')
        while True:
            localtime = datetime.datetime.now()                # 获取当前时间
            now = localtime.strftime('%H:%M:%S')
            self.send_message(receiver_class=0)
            self.send_message(receiver_class=1)
            self.send_message(receiver_class=2)
            self.send_message(receiver_class=3)
            self.cache_write()
            print(now)
            time.sleep(self.time_interval)
            if np.mod(time.localtime()[4], 15) == 0:
                itchat.send("wechat online", toUserName="filehelper")
            if time.time() >= self.next_reset_time:
                self.msg_send_num = self.daily_reset()
            if 21 > time.localtime()[3] > 16:
                time.sleep(60)
            if 9 > time.localtime()[3] > 3:
                time.sleep(60)


class send_email(object):
    def __init__(self, config_file='D:\\Python_Config\\Email_Send.json'):
        config = json.load(open(config_file, 'r'))
        self.sender = config['sender']
        self.smtpserver = config['smtpserver']
        self.username = config['username']
        self.password = config['password']

    def sends(self, receiver=["3285670383@qq.com"], title=u"邮箱提示系统",
             context="Hi!\nHow are you?\nI write this email to python"):
        for receiver_email in receiver:
            self.send(receiver_email, title, context)

    def send(self, receiver=["3285670383@qq.com"], title="Im Lwz",
             context="Hi!\nHow are you?\n"):
        # Create message container - the correct MIME type is multipart/alternative.
        if len(receiver) > 1:
            msg = MIMEMultipart('multipart')
        else:
            msg = MIMEMultipart('alternative')
            receiver = receiver[0]
        msg['Subject'] = title
        msg.attach(MIMEText(context, 'plain'))
        # Create the body of the message (a plain-text and an HTML version).
        msg['from'] = self.sender
        msg['to'] = receiver

        smtp = smtplib.SMTP()
        smtp.connect('smtp.163.com')
        smtp.login(self.username, self.password)
        smtp.sendmail(self.sender, receiver, msg.as_string())
        smtp.quit()
        print('email send to ', receiver, 'successful')


if __name__ == '__main__':
    sw = send_message_to_wechat()
    sw.wechat_login()                              # 扫描二维码并登陆
    sw.remind()                                    # 提醒模式
