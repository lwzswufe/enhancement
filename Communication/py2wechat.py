# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import itchat           # 需要用pip导入 itchat包
import datetime
import time
import json
import os
import numpy as np


class send_message_to_wechat(object):
    def __init__(self, time_interval=2.9,
                 msg_num_file='D:\\Python_Config\\WeChat_msg_num.json',
                 config_file='D:\\Python_Config\\WeChat_Send.json',
                 ):
        config = json.load(open(config_file, 'r'))
        self.time_interval = time_interval
        self.is_test = True
        if self.is_test:
            self.receiver = ["filehelper"]
        else:
            self.receiver = config['receiver']
        self.file_name = list()
        self.file_update_time = list()
        self.msg_send_num = list()
        self.is_change = list()
        self.file_exist = list()

        for i in range(len(config['file_name'])):
            fn_list = config['file_name'][i]
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
                self.file_name[i][key_name] = fn
                self.file_update_time[i][key_name] = 0    # 文件修改时间初始化
                self.msg_send_num[i][key_name] = 0        # 信息发送条数初始化

        print('initial over')
        self.msg_send_num = self.daily_reset()

    def daily_reset(self, reset_file='D:\\Python_Config\\WeChat_Send_reset.json'):
        fp = open(reset_file, 'r')
        reset_config = json.load(fp)
        fp.close()
        if reset_config['next_reset_time'] < time.time():
            next_time = time.time() + 86400 - np.mod(time.time() - 28800, 86400)  # 北京时间下午4点重置
            reset_config['next_reset_time'] = next_time
            reset_config['time_str'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(next_time))
            reset_config['msg_send_num'] = self.msg_send_num
            fp = open(reset_file, 'w')
            fp.write(json.dumps(reset_config))                                      # 重置文件//写入
            fp.close()
            for fn_list in self.file_name:                                          # 重置文件
                for fn in fn_list:
                    fp = open(fn, 'w')
                    fp.close()
            print('reset over')
        else:
            self.msg_send_num = reset_config['msg_send_num']                        # 载入缓存
            print('no reset')
        print('next reset time:  ' + reset_config['time_str'])
        return reset_config['msg_send_num']

    def wechat_login(self):                        # 自动登陆微信
        if self.is_test:
            print('本地测试开启')
        else:
            itchat.auto_login()
            print('微信登陆成功')

    def get_message(self, receiver_class=1):                         # 读取本地文件信息
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
                for context in contexts[self.msg_send_num[receiver_class][key_name]:]:  # 跳过已经推送的信息
                    self.wechat_push(context, receiver_class)                           # 推送信息
                    self.msg_send_num[receiver_class][key_name] += 1                    # 记录信息条数
                f.close()

    def cache_write(self, reset_file='D:\\Python_Config\\WeChat_Send_reset.json'):
        if sum(self.is_change) > 0:
            fp = open(reset_file, 'r')
            reset_config = json.load(fp)
            reset_config['msg_send_num'] = self.msg_send_num
            fp.close()

            fp = open(reset_file, 'w')
            fp.write(json.dumps(reset_config))                                      # 重置文件//写入
            fp.close()

    def wechat_push(self, context, receiver_class=1):  # 微信推送信息
        if self.is_test:
            print(context)
        else:
            for receiver in self.receiver[receiver_class]:
                itchat.send(context, toUserName=receiver)

    def remind(self):                              # 监控文件变化
        # self.wechat_push('Python_WeChat 已开始执行!')
        while True:
            localtime = datetime.datetime.now()    # 获取当前时间
            now = localtime.strftime('%H:%M:%S')
            try:
                self.get_message(receiver_class=0)
                self.get_message(receiver_class=1)
                self.cache_write()
                print(now)
                time.sleep(self.time_interval)
            except KeyboardInterrupt:
                self.wechat_push('Python_WeChat 已执行完毕！\n')
                break


if __name__ == '__main__':
    sw = send_message_to_wechat(
                                )
    sw.wechat_login()                              # 扫描二维码并登陆
    sw.remind()                                    # 提醒模式
