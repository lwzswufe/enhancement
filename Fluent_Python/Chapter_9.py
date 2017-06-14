# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
from array import array
import math

class Vector2d:
    typecode = 'd'

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    @property  # 特性 使得self.x不可修改 且self.x = self.__x
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self)  # 格式化显示

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):  # 生成实例的二进制表达式
        return (bytes([ord(self.typecode)]) +
                bytes(array(self.typecode, self)))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __hash__(self):  # 散列化
        return hash(self.x) ^ hash(self.y)

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def angle(self):  # 求角度
        return math.atan2(self.y, self.x)

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('p'):  # 弧度制
            fmt_spec = fmt_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = '<{}, {}>'
        else:
            coords = self
            outer_fmt = '({}, {})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(*components)  # *components 拆包

    @classmethod  # 类方法
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)


if __name__ == "__main__":
    v1 = Vector2d(3, 4)
    print(v1.x, v1.y)
    x, y = v1
    print(x, y)
    print(v1)
    v1_clone = eval(repr(v1))
    print(v1 == v1_clone)
    print(v1)
    print(bytes(v1))
    print(abs(v1))
    print(bool(v1), bool(Vector2d(0, 0)))
    print(Vector2d.frombytes(bytes(v1)))

    print(format(v1))
    print(format(v1, '.2f'))
    print(Vector2d(0, 0).angle())
    print(format(Vector2d(1, 1), '0.5fp'))