import QuoteSpi
import time
'''
运行前需要将 QuoteSpi.cpp 编译为 QuoteSpi.pyd 或 QuoteSpi.so
'''
print("module QuoteSpi:")
for key in QuoteSpi.__dict__.keys():
    print("{}:{}".format(key, QuoteSpi.__dict__[key]))
print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
from QuoteSpi import MarketData, QuoteSpi, BaseStrategy

print("class MarketData:")
for key in MarketData.__dict__.keys():
    print("{}:{}  {}".format(key, MarketData.__dict__[key], type(MarketData.__dict__[key])))
print("++++++++++++++++++++++++++++++++++++++++++++++++++++")

print("class BaseStrategy:")
for key in BaseStrategy.__dict__.keys():
    print("{}:{}".format(key, BaseStrategy.__dict__[key]))
print("++++++++++++++++++++++++++++++++++++++++++++++++++++")

print("class QuoteSpi:")
for key in QuoteSpi.__dict__.keys():
    print("{}:{}".format(key, QuoteSpi.__dict__[key]))
print("++++++++++++++++++++++++++++++++++++++++++++++++++++")

spi = QuoteSpi()

stg = BaseStrategy()
if spi.Register(stg):
    print("register successful")
else:
    print("register failed")

class UserStrategy(BaseStrategy):
    def OnMarket(self, data=MarketData()):
        s = "User Get:code:{} last_pr:{:.2f} b1pr:{:.2f} s1pr:{:.2f}".format(data.code, data.last_pr, data.b1_pr, data.s1_pr)
        pass



user_stg = UserStrategy()
spi.Register(user_stg)
no_stg = "   "
spi.Register(no_stg)

time_st = time.time()
count = 0
# 使用python循环调用策略与 使用C++调用策略差别不大
if True:
    data = spi.get()
    print("data type:{} code ".format(type(data)))
    while data is not None and count < 7:
        print(data.pcode, type(data.pcode))
        # print("code:{} last_pr:{:.2f} b1pr:{:.2f} s1pr:{:.2f}".format(data.ccode, data.last_pr, data.b1_pr, data.s1_pr))
        # print(data.str())
        for s in spi.StrategyList:
            s.OnMarket(data)
        # stg.OnMarket(data)
        # user_stg.OnMarket(data)
        count += 1
        data = spi.get()
# else:
#     spi.Start()
used_time = time.time() - time_st
print("program used:{:.3f}s".format(used_time))         # 程序结束 