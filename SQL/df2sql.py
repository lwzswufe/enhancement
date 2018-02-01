# author='lwz'
# coding:utf-8

import json
import pandas as pd
import pymysql as pysql


def log_in(fn='sql3.json'):
    with open(fn, 'r') as f:
        log_in_msg = json.load(f)

    conn = pysql.connect(host=log_in_msg['ip'], user=log_in_msg['user'],
                         passwd=log_in_msg['passwd'], database=log_in_msg['basename'],
                         charset='utf8')

    return conn


def get_dtypes(df_dtypes):
    dtypes = [d.name for d in df_dtypes]
    type_str = []
    for i in range(len(dtypes)):
        if 'int' in dtypes[i]:
            type_str.append('int')
        elif 'float' in dtypes[i]:
            type_str.append('float')
        else:
            type_str.append('str')

    return type_str


def get_row_value(values, dtype):
    row_str = ' '
    for i in range(len(values)):
        if dtype[i] == 'str':
            row_str += "'{}',".format(values[i])
        else:
            row_str += str(values[i]) + ','

    return row_str[:-1]


def upload_df(conn, df, tablename):
    '''
    insert into Student(S_StuNo,S_Name,S_Sex,S_Height)
    select '001','项羽','男','190' union
    select '002','刘邦','男','170' union
    select '003','貂蝉','女','180' union
    select '004','天明','男','155' union
    select '005','少司命','女','175'
    '''

    if len(df) == 0:
        print("df is empty")
        return

    cursor = conn.cursor()
    colnames = ','.join(df.columns)
    sql_order = "insert into {tablename}({colnames}) \nselect ".format(tablename=tablename, colnames=colnames)

    dtypes = get_dtypes(df.dtypes)
    values = []

    for idx in df.index:
        values .append(get_row_value(df.ix[idx], dtypes))

    sql_order += " union \n select ".join(values)

    print(sql_order)
    cursor.execute(sql_order)
    cursor.close()
    conn.commit()
    print("{} order data update over".format(len(df)))


def clean(conn, table_name):
    '''
    保留表结构并清空数据库
    :param conn:
    :param table_name:
    :return:
    '''
    cursor = conn.cursor()
    sql_order = 'truncate table ' + table_name
    cursor.execute(sql_order)
    print("successful clern table ", table_name)


if __name__ == "__main__":
    tablename = "exm"
    df = pd.read_csv("a.csv", dtype={"S_StuNo": str}, encoding='utf-8')
    conn = log_in()
    clean(conn, tablename)
    upload_df(conn, df, tablename)
