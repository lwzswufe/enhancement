import sys
import os
sys.path.append(os.path.abspath("."))
print(os.path.abspath("."))
import custom
import time

'''
运行前需要将 Custom.cpp 编译为 custom.pyd
'''
Donald_Trump = custom.Custom("Donald", "Trump", 1)          # __new__()  __init__()
Hillary_Clinton = custom.Custom("Hillary", "Clinton")       # __new__()  __init__()

del Hillary_Clinton                                         # __del__()
full_name = Donald_Trump.get_name()                         # 使用类方法
print(full_name)
Donald_Trump.change_name("Hillary", "Trump")
print("next")
full_name = Donald_Trump.get_name()  
print(full_name)
print("program  end.....")
