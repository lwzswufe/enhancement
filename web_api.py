# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import requests


headers = {"openid": "o8LXhwthhRUFzlKQxtjV1-qVoTlg", "first": "前面文字",
           "keyword1": "行情讯息", "keyword2": "2018-01-10 20:55:04",
           "remark": "后面文字", "tourl": ""}

url = "http://sw.sgytec.com/wxapi/api.php?action=sendwx"


data = {"comm": headers}  # 数据，这里使用的是Json格式进行传输
s = requests.Session()

r = requests.post(url, data=headers)
print('api return: ', r.text)


