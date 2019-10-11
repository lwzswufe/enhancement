import custom

Donald_Trump = custom.Custom("Donald", "Trump", 1)          # __new__()  __init__()
Hillary_Clinton = custom.Custom("Hillary", "Clinton", 1)    # __new__()  __init__()
del Hillary_Clinton                                         # __del__()
full_name = Donald_Trump.name()                             # 使用类方法
print(full_name)
print("program  end.....")
