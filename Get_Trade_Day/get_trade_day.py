# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import urllib.request as request
import datetime
'''
@query a single date: string '20170401';
@api return day_type: 0 workday 1 weekend 2 holiday -1 err
@function return day_type: 1 workday 0 weekend&holiday
'''


def get_day_type(query_date):
    url = 'http://tool.bitefu.net/jiari/?d=' + query_date
    resp = request.urlopen(url)
    content = resp.read()
    if content:
        try:
            day_type = int(content)
        except ValueError:
            return -1
        else:
            return day_type
    else:
        return -1


def is_tradeday(query_date):
    weekday = datetime.datetime.strptime(query_date, '%Y%m%d').isoweekday()
    if weekday <= 5 and get_day_type(query_date) == 0:
        return 1
    else:
        return 0


def today_is_tradeday():
    query_date = datetime.datetime.strftime(datetime.datetime.today(), '%Y%m%d')
    return is_tradeday(query_date)


def next_tradeday(time_type='str'):
    today = datetime.datetime.today()
    for i in range(1, 15):
        query_date = datetime.datetime.strftime(today + datetime.timedelta(i), '%Y%m%d')
        if is_tradeday(query_date):
            date = today + datetime.timedelta(i)
            break
    if time_type == 'str':
        return query_date
    elif time_type == 'timestamp':
        return date.timestamp()
    elif time_type == 'date':
        return date
    else:
        return i

if __name__ == '__main__':
    print(is_tradeday('20170406'))
    print(next_tradeday('num'))
    print(next_tradeday('timestamp'))
    print(next_tradeday('date'))