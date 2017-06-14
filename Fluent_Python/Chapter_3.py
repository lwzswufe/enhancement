# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
from types import MappingProxyType
from unicodedata import name


DIAL_CODES = [(86, 'China'), (91, 'India'), (1, 'United States'),
			(62, 'Indonesia'), (55, 'Brazil'), (92, 'Pakistan'),
			(880, 'Bangladesh'), (234, 'Nigeria'), (7, 'Russia'), (81, 'Japan')]
country_code = {country: code for code, country in DIAL_CODES}  # 字典推导
print(country_code)
country_code = {code: country.upper() for code, country in DIAL_CODES if code < 66}
print(country_code)

country_code.update({1: 'CHINA'})
country_code[0] = 'United States'
print(country_code)
print(country_code.get(22, 'not exist'))  # 给定查找缺失值
print(country_code.get(1, 'not exist'))
print(country_code.setdefault(7, []))  # 查找值 若缺失则设为default

d_proxy = MappingProxyType(country_code)  # 创建不可变映射
print(d_proxy)


set_a = {chr(i) for i in range(32, 256) if 'SIGN' in name(chr(i), '')}  # 集合推导
# 找到名字里含有sign的字符
print(set_a)
