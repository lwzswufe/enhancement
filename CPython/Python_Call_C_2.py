import cExm

'''
运行前需要将 g++ C_Code_Exm.h C_Code_Exm.c C_Decorate_Exm.c  -I C:\\Anaconda3\\include编译为 动态链接库 C_Exm.pyd
'''
print("python call cpp dll:")
cExm.test()
n = 5
c = cExm.fac(n)
print("factor({}) = {}".format(n, c))
s = "abcdefg"
return_s = cExm.doppel(s)
print("python put {}\n C return {}".format(s, return_s))