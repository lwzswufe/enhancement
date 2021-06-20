import Quote
from ctypes import Structure, c_char, c_double, pointer, POINTER, c_void_p, sizeof

'''
运行前需要将 Custom.cpp 编译为 custom.pyd
'''
# 测试数据结构体
class QuoteData(Structure):
    _fields_ = [("code", c_char * 7),
                ("last_pr", c_double),
                ("b1_pr", c_double),
                ("s1_pr", c_double),
                ("next", POINTER(c_void_p))
                ]
for key in Quote.QuoteAPI.__dict__.keys():
    print("{}:{}".format(key, Quote.QuoteAPI.__dict__[key]))
quote = Quote.QuoteAPI()
quote.initial()

return_type = POINTER(QuoteData)
# quote.get_struct.restype = return_type 
data = quote.get_struct()
struct_ptr = data
print("return ")
print("_{}_".format(hex(struct_ptr)))
print("size:{}".format(sizeof(struct_ptr)))
if struct_ptr != 0:
    print("code: {}".format(struct_ptr.code))


data = quote.get()
while data is not None:
    print("{} {:.2f} {:.2f} {:.2f}".format(*data))
    data = quote.get()
print("program  end.....")                                  # 程序结束 自动回收Donald_Trump 对象