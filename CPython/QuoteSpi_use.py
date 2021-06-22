import QuoteSpi
'''
运行前需要将 QuoteSpi.cpp 编译为 QuoteSpi.pyd 或 QuoteSpi.so
'''

for key in QuoteSpi.__dict__.keys():
    print("{}:{}".format(key, QuoteSpi.__dict__[key]))

from QuoteSpi import Read, Get, MarketData

Read()
data = Get()
print("type:{}".format(type(data)))
print("program  end.....")                                  # 程序结束 自动回收Donald_Trump 对象