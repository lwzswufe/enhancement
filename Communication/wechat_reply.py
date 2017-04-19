# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import pandas as pd


def reply_signal(msg=dict, wechat_class=None):
    try:
        context = msg['Text']
    except TypeError:
        print(msg)
    if context[0] != '#':
        return ''
    else:
        context = context[1:]

    if context == 'help':
        text = '请输入#开头的信息与我开始互动\n' +\
               '例如#600000 查询股票持仓'
        return text
    elif context.isdigit():
        return qurry_position(context)
    elif context == 'sendfile':
        wechat_class.send_wechat_file(mandatory_order=True)
    return ''


def reply_group(msg=dict, wechat_class=None):
    return reply_signal(msg, wechat_class)


def qurry_position(code=str, position_file='\\\\SWFUTURES-PC\\Share\\Trade\\macd_v2_position.csv'):
    df = pd.read_csv(position_file, dtype={'code': str})
    position_list = df.code
    df = df.set_index('code', drop=True)
    if code in set(position_list):
        context = code + ' 有持仓 买入时间 ' + str(df.buyday[code]) + ' 买入价格 ' +\
                  str(round(float(df.buyprice[code]), 2))
    else:
        context = code + ' 无持仓'
    return context


if __name__ == '__main__':
    text = reply_signal(msg={'Type': 'Text', 'Text': '#600010'})
    print(text)
