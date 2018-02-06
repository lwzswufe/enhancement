# author='lwz'
# coding:utf-8

import time
import timeit


'''
timeit(stmt='pass', setup='pass', timer=<built-in function perf_counter>, number=1000000, globals=None)
    Convenience function to create Timer object and call timeit method.
    stmt  = 主程序  主要测量运行时间的程序
    number= 重复次数
    setup = 运行主程序之前需要执行的语句如 数据，需要import的包

class Timer(builtins.object)
__init__(self, stmt='pass', setup='pass', timer=<built-in function perf_counter>, globals=None)
 |      Constructor.  See class doc string.
 |  timeit(self, number=1000000)
'''

t1 = timeit.Timer('sum(x)', 'x = (i for i in range(1000))')
print(t1.timeit(5))

t1 = timeit.Timer(stmt='sum(x)', setup='x = (i for i in range(1000))')
print(t1.timeit(5))

print(timeit.timeit('x=map(lambda x:x*10,range(32))'))