# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
s = 'São Paulo'
b = s.encode('utf8')     # 编码
print(b)
print(s.encode('latin'))
print(s.encode('latin'))
print(s.encode('cp437', errors='ignore'))  # 忽略错误值
print(s.encode('cp1252', errors='replace'))  # 将错误值替换为特殊符

print(b.decode('utf8'))  # 解码
print(b.decode('cp437', errors='ignore'))
print(b.decode('cp437', errors='replace'))
