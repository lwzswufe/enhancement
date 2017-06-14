# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
from array import array
import reprlib
import math
import numbers
import functools
import operator
import itertools  # <1>


class Vector:
    typecode = 'd'

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)  # 生成字符串
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(self._components))

    def __eq__(self, other):
        return (len(self) == len(other) and
                all(a == b for a, b in zip(self, other)))

    def __hash__(self):
        hashes = (hash(x) for x in self)
        return functools.reduce(operator.xor, hashes, 0)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):  # 设置getitem属性 方便切片
        cls = type(self)
        if isinstance(index, slice):  # 若是slice类 切片
            return cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            return self._components[index]
        else:
            msg = '{.__name__} indices must be integers'
            raise TypeError(msg.format(cls))

    shortcut_names = 'xyzt'

    def __getattr__(self, name):  # 动态设置属性 xyzt
        cls = type(self)
        if len(name) == 1:
            pos = cls.shortcut_names.find(name)
            if 0 <= pos < len(self._components):
                return self._components[pos]
        msg = '{.__name__!r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls, name))

    def __setattr__(self, name, value):  # 设置属性
        cls = type(self)
        if len(name) == 1:  # <1>
            if name in cls.shortcut_names:  # 禁止设置  x y z t
                error = 'readonly attribute {attr_name!r}'
            elif name.islower():  # <3>
                error = "can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''  # <4>
            if error:  # <5>
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        super().__setattr__(name, value)  # 默认情况 在超类上调用setattr方法

    def angle(self, n):  # h表示超球面坐标 p极坐标
        r = math.sqrt(sum(x * x for x in self[n:]))
        a = math.atan2(r, self[n-1])
        if (n == len(self) - 1) and (self[-1] < 0):
            return math.pi * 2 - a
        else:
            return a

    def angles(self):  # <3>
        return (self.angle(n) for n in range(1, len(self)))

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('h'):  # hyperspherical coordinates
            fmt_spec = fmt_spec[:-1]
            coords = itertools.chain([abs(self)],
                                     self.angles())  # <4>
            outer_fmt = '<{}>'  # <5>
        else:
            coords = self
            outer_fmt = '({})'  # <6>
        components = (format(c, fmt_spec) for c in coords)  # <7>
        return outer_fmt.format(', '.join(components))  # <8>

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)
# END VECTOR_V5


if __name__ == "__main__":
    v1 = Vector([3, 4, 5])
    x, y, z = v1
    print(x, y, z)
    print(v1)
    Vector([3.0, 4.0, 5.0])
    v1_clone = eval(repr(v1))
    print(v1_clone)
    print(v1 == v1_clone)
    print(v1)

    print(abs(v1))  # doctest:+ELLIPSIS
    print(bool(v1), bool(Vector([0, 0, 0])))
    v7 = Vector(range(7))
    print(v7)
    print(abs(v7))  # doctest:+ELLIPSIS

    v1 = Vector([3, 4, 5])
    print(len(v1))
    print(v1[0], v1[len(v1)-1], v1[-1])

    v7 = Vector(range(7))
    print(v7)
    print(v7[1:4])
    print(Vector([1.0, 2.0, 3.0]))
    print(v7[5])
    print(v7.y, v7.z, v7.t)