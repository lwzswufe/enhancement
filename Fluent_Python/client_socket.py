# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import socket


HOST = "127.0.0.1"
PORT = 8888
s = socket.create_connection(address=(HOST, PORT), timeout=5,)
# source_address=("127.0.0.1", 51011) # 可选参数 同一个链接 每个地址只能用一次

print("client: {}".format(s.getsockname()))

recv = s.recv(1024)
if recv == b"hello":
    print("connect to {}:{} successful".format(HOST, PORT))
else:
    print(recv)
    print("please start sever")
    raise ConnectionError

# 所有数据一定要以\n结尾
s.send(b"01\n")
print(s.recv(1024))  # 缓冲区大小
s.send(bytes("你好\n", encoding="utf-8"))
print(s.recv(1024))  # 缓冲区大小
s.send(b"hello\n")
print(s.recv(1024))  # 缓冲区大小 接受最近一条消息


s.close()
print("close connect")