# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import requests
import json
import pandas as pd

user_table = pd.read_csv('user2.txt', encoding='utf-8')
url = "http://czt.sgytec.com/wxapi/api.php?action=sendwx"
with open('api.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for i in range(len(user_table)):
    data['comm']['openid'] = user_table.user_id[i]
    print(data['comm']['openid'])
    name = user_table.user_name[i]
    b = json.dumps(data)
    r = requests.post(url, data=b)
    print(name, 'api return: ', r.text)


