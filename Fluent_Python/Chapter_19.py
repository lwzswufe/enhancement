# author='lwz'
# coding:utf-8
# !/usr/bin/env python3

from collections import abc
import keyword


class FrozenJSON():
    """
    从字典对象动态获取属性
    """
    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
                self.__data[key] = value
            else:
                self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJSON.build(self.__data[name])

    @classmethod
    def build(cls, obj):  # 类方法
        if isinstance(obj, abc.Mapping):
            return cls(obj)  # 返回类对象
        elif isinstance(obj, abc.MutableSequence):  # 列表
            return [cls.build(item) for item in obj]
        else:
            return obj


class LineItem():
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    @property
    def weight(self):
        return self.__weight

    @weight.setter  # 设值方法
    def weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')


def quantity(storage_name):  # 特性工厂函数
    # type(instance) =  __main__.LineItem2
    # instance 甚至可以用self来代替 它表示实例
    def qty_getter(instance):   #  特性取值函数
        return instance.__dict__[storage_name]

    def qty_setter(instance, value):  # 特性设值函数
        if value > 0:
            instance.__dict__[storage_name] = value

    return property(qty_getter, qty_setter)
    # 特性构造方法函数
    # property(fget=None, fset=None, fdel=None, doc=None)


class LineItem_2:
    weight = quantity('weight')
    price = quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

if __name__ == "__main__":
    f = FrozenJSON({"name_": "scr", "_id":  1})
    print(f.__dict__)

    walnuts = LineItem('walnuts', 1, 10.00)
    walnuts = LineItem_2('walnuts', 1, 10.00)

