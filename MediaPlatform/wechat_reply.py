# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import json


class auto_reply(object):
    def __init__(self, config_file='D:\\Python_Config\\WeChat_reply.json'):
        config = json.load(open(config_file, 'r', encoding="utf-8"))
        self.position_file_name = config['position_file_name']
        self.stock_signal_file_name = config['stock_signal_file_name']
        self.stock_signal_keyname = config['stock_signal_keyname']
        self.buy_signal_file_name = config['buy_signal_file_name']
        self.sell_signal_file_name = config['sell_signal_file_name']
        self.stock_signal_update_time = list()
        self.stock_position = list()
        self.stock_buy_table = list()
        self.stock_sell_table = list()

    def reply_signal(self, msg=dict, wechat_class=None):
        try:
            context = msg['Text']
            texts = self.reply(context, wechat_class)
            if len(texts) > 0:
                return texts
        except TypeError:
            print(msg)

    def reply(self, context=str):
        context = context.lower()
        if context == 'help':
            texts = '请输入信息与我开始互动(若在群聊中清以#开头)\n查询股票持仓：\n' +\
                    '超短线 sxxxxxx \n小时线 hxxxxxx \n日线 dxxxxxx\n' +\
                    '查询今日股票信号：\n' +\
                    '超短线买入 sbuy\n超短线卖出 ssell\n' +\
                    '小时线买入 hbuy\n小时线卖出 hsell\n' +\
                    '日线买入   dbuy\n日线卖出   dsell\n'
        else:
            texts = '输入错误 请输入help获取命令列表'
        print(texts)
        return texts