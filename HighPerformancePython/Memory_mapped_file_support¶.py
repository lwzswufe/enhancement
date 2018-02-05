# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
'''
 mmap是一种虚拟内存映射文件的方法，即将一个文件或者其它对象映射到进程的地址空间
 ，实现文件磁盘地址和进程虚拟地址空间中一段虚拟地址的一一对映关系。

1，创建：创建并返回一个 mmap 对象m

m=mmap.mmap(fileno, length[, flags[, prot[, access[, offset]]]])
fileno： 文件描述符，可以是file对象的fileno()方法，或者来自os.open()
        ，在调用mmap()之前打开文件，不再需要文件时要关闭。

View Code
length：要映射文件部分的大小（以字节为单位），这个值为0，则映射整个
        文件，如果大小大于文件当前大小，则扩展这个文件。

flags：MAP_PRIVATE：这段内存映射只有本进程可用；
mmap.MAP_SHARED：将内存映射和其他进程共享，所有映射了同一文件的进程
                ，都能够看到其中一个所做的更改；

prot：mmap.PROT_READ, mmap.PROT_WRITE 和 mmap.PROT_WRITE | mmap.PROT_READ。最后一者的含义是同时可读可写。

access：在mmap中有可选参数access的值有

ACCESS_READ：读访问。

ACCESS_WRITE：写访问，默认。

ACCESS_COPY：拷贝访问，不会把更改写入到文件，使用flush把更改写到文件。
http://www.cnblogs.com/zhoujinyi/p/6062907.html
'''

import os
import mmap

m = mmap.mmap(os.open('trade.log', os.O_RDWR), 0)

print('First 10 bytes via read :', m.read(10))
print('First 10 bytes via slice:', m[:10])
print('2nd   10 bytes via read :', m.read(10))

print("当前光标位置:", m.tell())
m.seek(0)  # 移动光标
print("当前光标位置:", m.tell())
m.write(b'\x00')  # 写入数据 覆盖
m.write(b"Load data to memory agine\n")
print(m[:].decode("utf-8"))


m = mmap.mmap(-1, 64)
print('First 1 bytes via read :', m.read_byte())
m.seek(0)
m.write_byte(13)
m.seek(0)
print('First 1 bytes via read :', m.read_byte())
print("当前光标位置:", m.tell())
m.write(b'\x00')  # 写入数据
m.write(b"Load data to memory agine\n")
print(m[:].decode("utf-8"))

