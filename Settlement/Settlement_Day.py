# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import os
import pandas as pd


def Read_Settlement(fn):
    f = open(fn, 'r', encoding='gbk')
    line = 'start '
    Attr = dict()
    Dict = {
            'Transaction_Record': pd.DataFrame(),
            'Position_Closed': pd.DataFrame(),
            'Positions_Detail': pd.DataFrame(),
            'Positions': pd.DataFrame()
            }

    while line:
        line = f.readline()
        line_type = get_information_type(line)
        if line_type == '':
            pass
        elif len(line_type) > 4:
            f, Dict[line_type] = get_trade_msg(f)
        elif line_type == 'msg':
            Attr.update(get_message(line))

    f.close()
    s = pd.Series(Attr)
    df = pd.DataFrame()
    df[0] = s
    Dict['Attr'] = df.transpose()
    if len(Dict['Positions']) > 0:
        Dict['Positions']['Date'] = Attr['Date']
    elif len(Dict['Positions_Detail']) > 0:
        Dict['Positions_Detail']['Date'] = Attr['Date']

    return Dict


def get_trade_msg(f):
    Skip_line(f, 5)
    line = f.readline()
    line = line.replace(" ", '')
    columns = line.split("|")[1:-1]
    Skip_line(f, 3)
    df = pd.DataFrame()
    flag = 0
    line = f.readline()
    while line:
        if "------------------------" in line:
            break

        values = line.split("|")[1:-1]
        s = pd.Series(dict(zip(columns, values)))
        df[flag] = s
        flag += 1
        Skip_line(f, 1)
        line = f.readline()

    return f, df.transpose()


def get_message(line=u'客户号 Client ID：  800491          客户名称 Client Name：宏鑫\n'):
    '''
    识别行数据中的账户信息
    :param line: u'客户号 Client ID：  800491          客户名称 Client Name：宏鑫\n'
    :return: {ClientID:800491,  ClientName：宏鑫}
    '''
    line = line.replace(' ', '')
    line = line.replace('\n', '：')
    key_list = list()
    value_list = list()
    msg = ''
    flag = 0
    for x in line:
        if ord(x) < 255:
            msg += x
        elif len(msg) > 0:
            flag += 1
            if flag % 2 == 1:
                key_list.append(msg)
            else:
                value_list.append(msg)
            msg = ''

    if 'ClientName' in key_list:
        value_list.append(line.split('：')[-2])

    return dict(zip(key_list, value_list))


def Skip_line(f, nrow=1):
    if nrow == 1:
        f.readline()
    else:
        for i in range(nrow):
            f.readline()


def get_information_type(line):
    if len(line) < 5:
        return ''
    elif 'Transaction Record' in line:
        return 'Transaction_Record'
    elif 'Position Closed' in line:
        return 'Position_Closed'
    elif 'Positions Detail' in line:
        return 'Positions_Detail'
    elif 'Positions' in line:
        return 'Positions'
    elif '：' in line:
        return 'msg'
    return ''


def read_files(path):
    files = os.listdir(path)
    files = [fn for fn in files if (len(fn) > 15 and fn[4:-4].isdigit())]
    print(files)
    Dicts = {
            'Attr': list(),
            'Transaction_Record': list(),
            'Position_Closed': list(),
            'Positions_Detail': list(),
            'Positions': list()
            }

    for fn in files:
        Dict = Read_Settlement(path+fn)
        for key in Dict.keys():
            Dicts[key].append(Dict[key])

    for key in Dicts.keys():
        df = pd.concat(Dicts[key], axis=0, ignore_index=True)
        df.to_csv(key + '.csv', encoding='gbk', index=False)


if __name__ == "__main__":
    # get_message()
    read_files('D:\\data\\settlement\\')
    # Read_Settlement("D:\\data\\settlement\\结算单_20180125.txt")