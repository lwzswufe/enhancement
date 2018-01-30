# author='lwz'
# coding:utf-8
import dis
from HighPerformancePython import Julia_set_00


'''
dis模块主要是用来分析字节码的一个内置模块，经常会用到的方法是dis.dis([bytesource])，
参数为一个代码块，可以得到这个代码块对应的字节码指令序列。


https://www.rddoc.com/doc/Python/3.6.0/zh/library/dis/

class dis.Bytecode(x, *, first_line=None, current_offset=None)
分析对应于函数，生成器，方法，源代码字符串或代码对象（由 compile() 返回）的字节码。
这是下面列出的许多函数的一个方便的包装，最着名的是 get_instructions()，作为在 Bytecode
实例上的迭代产生作为 Instruction 实例的字节码操作。如果 first_line 不是 None，则它指示
应该为拆卸的代码中的第一源行报告的行号。否则，源行信息（如果有的话）直接取自已拆解的代码对象。
如果 current_offset 不是 None，则它指的是在反汇编代码中的指令偏移量。设置这意味着 dis()
将针对指定的操作码显示“当前指令”标记。

classmethod from_traceback(tb)
从给定的追溯构建 Bytecode 实例，将 current_offset 设置为负责异常的指令。

codeobj
编译的代码对象。

first_line
代码对象的第一个源代码行（如果可用）

dis()
返回字节码操作的格式化视图（与 dis.dis() 打印的相同，但返回为多行字符串）。

info()
返回格式化的多行字符串，其中包含有关代码对象的详细信息，如 code_info()。

dis.dis(x=None, *, file=None)
拆卸 x 对象。 x 可以表示模块，类，方法，函数，生成器，代码对象，源代码字符串或原始字节码的字节序列。
对于模块，它会拆散所有函数。对于一个类，它反汇编所有的方法（包括类和静态方法）。对于代码对象或原始
字节码序列，每个字节码指令打印一行。字符串首先被编译为使用 compile() 内置函数代码对象，然后被
反汇编。如果没有提供对象，则此函数将反汇编最后一个回溯。


第一列 25代码长度（行数）
第二列 >>指向其他代码的跳转点
第三列 地址与操作名
第四列 操作参数
第五列 标记与原始Python参数
'''

print(dis.dis(Julia_set_00))