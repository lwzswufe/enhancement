# author='lwz'
# coding:utf-8
# !/usr/bin/env python3


class A(object):
    name = 'A'
    name_list = list()

    def __init__(self, code):
        self.code = code
        self.stock_list = list()

    def disp(self):
        print('name- {} code- {} stock_list- {} name_list- {}'
              .format(self.name, self.code, self.stock_list, self.name_list))


class B(A):
    name = 'A'

    def disp(self):
        print('name= {} code= {} stock_list= {} name_list= {}'
              .format(self.name, self.code, self.stock_list, self.name_list))


class C(A):
    name = 'A'

    def disp(self):
        print('name: {} code: {} stock_list: {} name_list: {}'
              .format(self.name, self.code, self.stock_list, self.name_list))


if __name__ == '__main__':
    a = A('600001')
    b = B('600002')
    c = C('600003')
    l = [a, b, c]
    a.name_list.append('1')
    b.name_list.append('2')
    b.name = 'B'
    c.name = 'C'
    print("直接定义的属性会在不同类之间共享， 我们对a b的name_list(因为默认为list()) 进行的操作会直接同步到 a b c中去")
    print("例如对a增加元素 '1' b c也会增加元素 '1' ")
    c.stock_list.append('3')

    for cla in l:
        cla.disp()

    b.name = 'p'
    a.name_list.pop(1)
    print("例如对a删除元素 '2' b c也会删除元素 '2' ")
    for cla in l:
        cla.disp()

    b.name_list = 'err'
    print("b.name_list 赋值成其他对象后 b.name_list 不再和a c绑定 ")
    for cla in l:
        cla.disp()
