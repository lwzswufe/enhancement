# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import json


f_name = 'D:\\Cache\\name.json'
f_name2 = 'D:\\Cache\\name2.json'
fp = open(f_name)
name = json.load(fp)                   # dict  read
print(name)
fp.close()

fp2 = open(f_name2, 'w')
obj = [[1, 2, 3], 123, 123.123, 'abc', {'key1': (1, 2, 3), 'key2': (4, 5, 6)}]
encoded_json = json.dumps(obj)    # change to json object
fp2.write(encoded_json)           # write json object
print(encoded_json)
# print(json.load(fp2))
fp2.close()

fp3 = open(f_name2, 'r')
read_text = json.load(fp3)
print(read_text)
fp3.close()
