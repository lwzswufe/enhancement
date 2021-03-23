import pandas as pd
from pymongo import MongoClient as mc
import time


'''
100万
               储存空间   写入时间  读取整表  读取单一股票  判断
字符串数据      38621184  29秒       8.10      0.788      3.373
整数           37322752  28秒        7.60      0.747      3.388
整数无所引     18661376  22秒        7.638      0.829      3.399

100万
               储存空间   写入时间  读取整表  读取单一股票  判断
字符串数据      38621184  29秒       8.10      0.788      3.373
整数           37322752  28秒        7.60      0.747      3.388
整数无所引     18661376  22秒        7.638      0.829      3.399
'''


def login():
    client = mc('localhost', 27017)
    return client


def readtxt(read_num=1000):
    filename = "E:\\data\\L2_data\\2020\\0219\\am_hq_order_spot.txt"
    data_list = []
    time_st = time.time()
    with open(filename, "r") as f:
        line_num = 0
        line = f.readline()
        while len(line) > 0 and line_num < read_num:
            line_num += 1
            words = line.split("\t")
            if len(words) > 14:
                data = [words[1], int(words[5]), int(words[7]), words[8], float(words[10]), int(words[11]), words[13], words[14]]
                # data = [words[1], int(words[5]), int(words[7]), words[8], float(words[10]), int(words[11]), int(words[13]), int(words[14])]
                data_list.append(data)
            line = f.readline()
    used_time = time.time() - time_st
    print("read:{} data:{} used:{:.3f}s".format(line_num, len(data_list), used_time))
    time_st = time.time()
    columns = ["datatime", "channel", "seq", "code", "price", "vol", "side", "type"]
    df = pd.DataFrame(data_list, columns=columns)
    df["datatime"] = pd.to_datetime(df["datatime"], format="%Y%m%d%H%M%S%f")
    print(df.head())
    used_time = time.time() - time_st
    print("generator DataFrame data:{} used:{:.3f}s".format(len(data_list), used_time))
    return df


def insert(client, df):
    basename = 'tick'
    # tablename = "no_index"
    tablename = "str_"
    db = client.get_database(basename)  # 创建base
    table = db.get_collection(tablename)  # 获取表
    # 判断数据表是否存在
    if table.estimated_document_count() > 0:
        # 若数据库已存在就清空数据表
        table.delete_many({})
    else:
        # 创建索引
        res = table.create_index([("seq", 1), ("code", 1)])
        pass
    insert_data = df.to_dict('records')
    time_st = time.time()
    table.insert_many(insert_data)
    used_time = time.time() - time_st
    print("insert data:{} used:{:.3f}s".format(len(df), used_time))


def query(client, tablename):
    basename = 'tick'
    db = client.get_database(basename)  # 创建base
    table = db.get_collection(tablename)  # 获取表
    # query all
    time_st = time.time()
    cursor = table.find({})
    df = pd.DataFrame(list(cursor))
    used_time = time.time() - time_st
    print("{} query all data:{} used:{:.3f}s".format(tablename, len(df), used_time))
    # query single code
    time_st = time.time()
    cursor = table.find({"code": "300817"})
    df = pd.DataFrame(list(cursor))
    used_time = time.time() - time_st
    print("{} query single data:{} used:{:.3f}s".format(tablename, len(df), used_time))
    # query side
    time_st = time.time()
    if tablename.find("str") >= 0:
        cursor = table.find({"side": "1"})
    else:
        cursor = table.find({"side": 1})
    df = pd.DataFrame(list(cursor))
    used_time = time.time() - time_st
    print("{} query one side data:{} used:{:.3f}s".format(tablename, len(df), used_time))


def insert_test():
    df = readtxt(5000000)
    client = login()
    for i in range(3):
        insert(client, df)


def query_test():
    client = login()
    for tablename in ["int", "no_index", "str_"]:
        for i in range(3):
            query(client, tablename)


if __name__ == "__main__":
    insert_test()
    # query_test()
