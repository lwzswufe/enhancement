# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
'''
转义符\r就可以把光标移动到行首而不换行
转义符\n就把光标移动到行首并且换行
转义符\b是退格键，也就是说把输出的光标往回退格子
'''
import sys,time
j = '#'
s = ['-', '\\', '|', '/']


if __name__ == '__main__':
    for i in range(101):
        string = 'loading... ' + str(i) + s[i % 4]
        print(string, end='')  # 不换行
        print('\b' * len(string), end='', flush=True)  # 删除前面打印的字符
        time.sleep(0.1)

    for i in range(1,61):
        j += '#'
        sys.stdout.write(str(int((i/60)*100))+'%  ||'+j+'->'+"\r")
        sys.stdout.flush()
        time.sleep(0.1)