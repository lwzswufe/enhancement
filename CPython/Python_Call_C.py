import ctypes

'''
运行前需要将 C_dll.c 编译为 动态链接库 C_dll.so
'''
dll = ctypes.cdll.LoadLibrary
lib = dll("./C_dll.so")
print("python call cpp dll:")
c = lib.add_func(2,3)
print("python get sum:{}".format(c))
