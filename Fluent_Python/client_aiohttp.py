# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import requests, json


url = 'http://127.0.0.1:8888/post/'

body = json.dumps({0: u"feed the api"})
r = requests.post(url=url, data=body)
print(r.content)

url = 'http://127.0.0.1:8888/put/'
r = requests.put(url=url, data=b"sdad")
print(r.content)

url = 'http://127.0.0.1:8888/get/1'
r = requests.get(url=url)
print("msg:", r.content)

url = 'http://127.0.0.1:8888/get/'
r = requests.get(url=url)
print("msg:", r.content)




