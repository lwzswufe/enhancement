# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import unittest
from Unit_test.Dict import Dict


'''
编写单元测试时，我们需要编写一个测试类，从unittest.TestCase继承。

以test开头的方法就是测试方法，不以test开头的方法不被认为是测试方法，测试的时候不会被执行。

对每一类测试都需要编写一个test_xxx()方法。由于unittest.TestCase提供了很多内置的条件判断，
我们只需要调用这些方法就可以断言输出是否是我们所期望的。最常用的断言就是assertEqual()：

包括测试前准备环境的搭建(setUp)，执行测试代码(run)，以及测试后环境的还原(tearDown)

每一个以test开头的方法，都会为其构建TestCase对象
'''


class TestDict(unittest.TestCase):
    def setUp(self):
        # 测试前准备环境的搭建(setUp)
        print('setUp...', self.__dict__['_testMethodName'])

    def tearDown(self):
        # 以及测试后环境的还原(tearDown)
        print('tearDown', self.__dict__['_testMethodName'])

    def test_init(self):
        d = Dict(a=1, b='test')
        self.assertEqual(d.a, 1)
        # 断言输出是否是我们所期望的
        self.assertEqual(d.b, 'test')
        self.assertTrue(isinstance(d, dict))

    def test_key(self):
        d = Dict()
        d['key'] = 'value'
        self.assertEqual(d.key, 'value')

    def test_attr(self):
        d = Dict()
        d.key = 'value'
        self.assertTrue('key' in d)
        self.assertEqual(d['key'], 'value')

    def test_keyerror(self):
        d = Dict()
        # 另一种重要的断言就是期待抛出指定类型的Error，比如通过d['empty']访问不存在的key时，断言会抛出KeyError
        with self.assertRaises(KeyError):
            value = d['empty']

    def test_attrerror(self):
        d = Dict()
        with self.assertRaises(AttributeError):
            value = d.empty

    def test_no_op(self):
        pass

if __name__ == '__main__':
    unittest.main()
