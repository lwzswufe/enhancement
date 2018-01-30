# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import telnetlib


HOST = "127.0.0.1"
PORT = 2323
t = telnetlib.Telnet()
t.open(HOST, PORT)
socket_ = t.get_socket()
print("client: {}".format(socket_.getsockname()))
# print("sever: {} client: {}".format(socket_.laddr, socket_.raddr))
print("connect to {}:{} successful".format(HOST, PORT))

# 所有数据一定要以\n结尾
t.write(b"01\n")
print(t.read_some())

t.write(bytes("你好\n", encoding="utf-8"))
print(t.read_some())

t.write(b"hello\n")
print(t.read_some())

t.close()
print("close connect")
