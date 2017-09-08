# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
'''
收集整理荐股情况
'''

import pandas as pd
import datetime
import os

class recommender(object):
    def __init__(self, df_fname='D:\\Cache\\Trade\\RecommendHistory.csv',
                 notice_fanme='D:\\Share\\Trade\\Recommend.txt'):
        self.context = ''
        self.df_fname = df_fname
        self.notice_fanme = notice_fanme
        if os.path.exists(self.df_fname):
            self.df = pd.read_csv(self.df_fname, dtype={'code':str}, encoding='gbk')
        else:
            columns = ['recommender', 'buyorsell', 'code', 'name', 'date', 'time_str', 'price', 'stop_win', 'stop_loss']
            self.df = pd.DataFrame(columns=columns)

    def append(self, code:'600000', name:str, price:10.01, buyorsell:'buy', recommender='test', arrs=[]):
        if not code.isdigit():
            if name.isdigit() and len(name) == 6:
                name, code = code, name
            else:
                return '股票代码错误，请输入六位数字'

        if len(code) != 6:
            return '股票代码长度错误'

        date = datetime.datetime.now().strftime("%Y-%m-%d")

        if buyorsell == '卖出' or buyorsell == 'sell':
            if len(self.df) == 0:
                return '{} 无持仓'.format(code)

            df = self.df[(self.df.code == code) & (self.df.recommender == recommender)
                        & (self.df.date != date)]
            if len(df) % 2 == 0:
                return '{} 无持仓'.format(code)
        elif buyorsell == '买入' or buyorsell == 'buy':
            df = self.get_today_data(recommender=recommender)
            if len(df) > 0:
                df2 = df[(df.buyorsell == '买入') | (df.buyorsell == 'buy')]
                if len(df2) > 0 and code in df2.code:
                    return '今日已买入{}'.format(code)

        price = round(float(price), 2)
        time_str = datetime.datetime.now().strftime("%H:%M:%S")

        columns = ['recommender', 'buyorsell', 'code', 'name', 'date', 'time_str', 'price', 'stop_win', 'stop_loss']
        if '止盈' in arrs:
            stop_win = round(float(arrs[arrs.index('止盈') + 1]), 2)
        else:
            stop_win = 0
        if '止损' in arrs:
            stop_loss = round(float(arrs[arrs.index('止损') + 1]), 2)
        else:
            stop_loss = 0

        df_add = pd.DataFrame([recommender, buyorsell, code, name, date, time_str, price, stop_win, stop_loss], index=columns).T

        if len(self.df) > 0:
            self.df = self.df.append(df_add, ignore_index=True)
        else:
            self.df = df_add

        self.df.to_csv(self.df_fname, index=False)
        context = buyorsell + ' ' + code + '\n'
        return '成功推荐股票{name}{code}'.format(name=name, code=code)
        # self.write(context)

    def write(self, context):
        if len(context) > 0:
            f = open(self.notice_fanme, 'a')
            f.write(context)
            f.close()

    def get_position_data(self, recommender=None, non_recommender='test'):
    #  舍弃重复前项 留下最后一项
        if recommender is None:
            df = self.df[(self.df.recommender != non_recommender)].drop_duplicates('code', keep='last')
            return df[(df.buyorsell == '买入') | (df.buyorsell == 'buy')]
        else:
            df = self.df[(self.df.recommender == recommender)].drop_duplicates('code', keep='last')
            return df[(df.buyorsell == '买入') | (df.buyorsell == 'buy')]

    def get_today_data(self, recommender=None, non_recommender='test'):
    # 获取今日荐股 分析师查看自己的 管理者查看全部
        today = datetime.datetime.now().strftime("%F")

        if recommender is None:
            df = self.df[(self.df.date == today) & (self.df.recommender != non_recommender)]
        else:
            df = self.df[(self.df.date == today) & (self.df.recommender == recommender)]

        return df

    def get_all_data(self, recommender=None, non_recommender='test'):
    # 获取所有荐股 分析师查看自己的 管理者查看全部
        if recommender is None:
            df = self.df[(self.df.recommender != non_recommender)]
        else:
            df = self.df[(self.df.recommender == recommender)]

        return df

    def update(self, code, stoporloss, price, recommender):
        if len(self.df) == 0:
            return '{} 无持仓'.format(code)

        df = self.df[(self.df.code == code) & (self.df.recommender == recommender)]
        if len(df) % 2 == 0:
            return '{} 无持仓'.format(code)

        if stoporloss == '止盈':
            self.df.loc[df.index[-1], 'stop_win'] = price
            self.df.to_csv(self.df_fname, index=False)
            return '成功更新{code}止盈价为{price}'.format(code=code, price=price)
        elif stoporloss == '止损':
            self.df.loc[df.index[-1], 'stop_loss'] = price
            self.df.to_csv(self.df_fname, index=False)
            return '成功更新{code}止损价为{price}'.format(code=code, price=price)

    def remove(self, code, recommender):
        df = self.get_today_data(recommender=recommender)
        idxs = df[df.code == code].index
        if len(idxs) > 0:
            self.df.drop(idxs, inplace=True)
            self.df.to_csv(self.df_fname, index=False)
            return '成功删除推荐记录'
        else:
            return '我们没有找到关于 {} 的推荐记录'.format(code)


if __name__ == '__main__':
    r = recommender()
    r.get_position_data()