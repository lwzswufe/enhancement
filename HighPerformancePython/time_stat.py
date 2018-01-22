# author='lwz'
# coding:utf-8
import cProfile
import pstats
import os
import sys
file_path = os.path.split(os.path.realpath(__file__))[0]
print("当前文件路径：", file_path)
sys.path.append(file_path)
# from HighPerformancePython.Julia_set_00 import calc_pure_python


print('使用cProfile分析的结果可以输出到指定的文件中，但是文件内容是以二进制的方式保存的，\n'
      '用文本编辑器打开时乱码。所以，Python提供了一个pstats模块，用来分析cProfile输出的文件内容。')
# 直接把分析结果打印到控制台
# cProfile.run("calc_pure_python(desired_width=1000, max_iterations=300)")
# 把分析结果保存到文件中
# cProfile.run("calc_pure_python(desired_width=1000, max_iterations=300)", filename="result.out")
# 增加排序方式
# cProfile.run("calc_pure_python(desired_width=1000, max_iterations=300)", filename="result.out", sort="cumulative")
print('stat.........\n'
      '.............\n'
      '.............\n')

# 创建Stats对象
p = pstats.Stats(file_path + "\\result.out")

p.strip_dirs()   # : 去掉无关的路径信息
p.sort_stats()   # : 排序，支持的方式和上述的一致
print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>分析结果>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
p.print_stats()  # : 打印分析结果，可以指定打印前几行
print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>函数被调用分析结果>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
p.print_callers()  # : 打印分析结果，可以指定打印前几行
print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>函数调用分析结果>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
p.print_callees()  # : 打印分析结果，可以指定打印前几行
