import QuoteSpi
'''
运行前需要将 QuoteSpi.cpp 编译为 QuoteSpi.pyd 或 QuoteSpi.so
'''
print("module QuoteSpi:")
for key in QuoteSpi.__dict__.keys():
    print("{}:{}".format(key, QuoteSpi.__dict__[key]))
print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
from QuoteSpi import MarketData, QuoteSpi

print("class MarketData:")
for key in MarketData.__dict__.keys():
    print("{}:{}".format(key, MarketData.__dict__[key]))
print("++++++++++++++++++++++++++++++++++++++++++++++++++++")

print("class QuoteSpi:")
for key in QuoteSpi.__dict__.keys():
    print("{}:{}".format(key, QuoteSpi.__dict__[key]))
print("++++++++++++++++++++++++++++++++++++++++++++++++++++")

spi = QuoteSpi()
data = spi.get()
print("data type:{} code ".format(type(data)))
while data is not None:
    print("code:{} last_pr:{:.2f} b1pr:{:.2f} s1pr:{:.2f}".format(data.code, data.last_pr, data.b1_pr, data.s1_pr))
    print(data.str())
    data = spi.get()

print("program  end.....")                                  # 程序结束 自动回收Donald_Trump 对象