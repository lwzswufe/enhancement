# author='lwz'
# coding:utf-8

'''
进入MongoDB所在文件夹 将配置文件conf放在bin所在目录
进入bin 启动mongod.exe
'''

import odo
import pandas as pd
from pymongo import MongoClient as mc

client = mc('localhost', 27017)
basename = 'tick'
print(client.database_names())  # 获取base名称
db = client.get_database('tick')  # 创建base
db.collection_names()  # table 集合
table = db.create_collection('SH600000')  # 创建表
table = db.get_collection('SH600000')  # 获取表
