import ctypes

'''
运行前需要将 C_dll.c 编译为 动态链接库 C_dll.so
'''
dll = ctypes.cdll.LoadLibrary
lib = dll("./cExm.so")
print("python call cpp dll:")
lib.cExm_test()
n = 5
c = lib.fac(n)
print("factor({}) = {}".format(n, c))
s = "abcdefg"
return_s = lib.doppel(s)
print("python put {}\n C return {}".format(s, return_s))