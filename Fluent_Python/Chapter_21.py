# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
from collections import namedtuple
import abc


print("###############file start##############\n")


def record_factory(cls_name, field_names):
    field_names = field_names.split(',')
    field_names = tuple(field_names)
    # 也可以使用__slots__ 替代 __slotss__

    def __init__(self, *args, **kwargs):
        attrs = dict(zip(self.__slotss__, args))
        attrs.update(kwargs)

        for name, value in attrs.items():
            setattr(self, name, value)

    def __iter__(self):
        for name in self.__slotss__:
            yield getattr(self, name)

    def __repr__(self):
        values = ', '.join('{}={!r}'.format(*i) for i in zip(self.__slotss__, self))
        return '{}({})'.format(self.__class__.__name__, values)

    cls_attrs = dict(__slotss__=field_names,
                     __init__=__init__,
                     __iter__=__iter__,
                     __repr__=__repr__)

    return type(cls_name, (object,), cls_attrs)


class AutoStorage:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class Validated(abc.ABC, AutoStorage):
    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validate(self, instance, value):
        """return validated value or raise ValueError"""


class Quantity_6(Validated):
    """
    继承 NonBlank 《—— Validated 《—— AutoStorage
    a number greater than zero
    """
    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value


class NonBlank(Validated):
    """a string with at least one non-space character"""
    def validate(self, instance, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError('value cannot be empty or blank')
        return value


def entity(cls):
    print("类装饰器属性:", cls.__dict__.items())
    print("enyity _init_")
    for key, attr in cls.__dict__.items():
        if isinstance(attr, Validated):
            type_name = type(attr).__name__
            attr.storage_name = '_{}#{}'.format(type_name, key)
            print("类名: {}, 类属型: {}".format(type_name, key))
    return cls


@entity
# ent会接受一个cls(定义) 即LineItem_6 并修改其属性再返回cls(定义)
# 随后cls会执行_init_ 实例化
class LineItem_6:
    description = NonBlank()
    weight = Quantity_6()
    price = Quantity_6()
    print("LineItem_6:load over")

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price
        print("LineItem_6:_init_ over")

    def subtotal(self):
        return self.weight * self.price


if __name__ == "__main__":
    print('\n#############__main__ start##############\n')
    print("因为类的定义体属于顶层对象 所以LineItem_6\n"
          "以及相关程序虽然在 main的后半部 \n但是他们会优先执行"
          "顶层程序执行完毕后执行 main 部分")
    Point = namedtuple('Point', ['x', 'y'])
    #                  类名      属性名
    print("namedtuple('类名', [属性名])")
    p = Point(11, y=22)
    print(p.x, p.y)

    MyClass = type('MyClass', (Point,),
            {'x': 42, 'y': lambda self: self.x * 2})
    print("type(类名, (父类), {属性名:属性值})")
    print(MyClass.x, MyClass.y)

    mc = type('MyClass', (object,),
            {'x': 42, 'y': lambda self: self.x * 2})
    print(mc.x, mc.y)

    Dog = record_factory('Dog', 'name,weight,owner')
    rex = Dog('Rex', 30, 'Bob')

    raisins = LineItem_6('Golden raisins', 10, 6.95)
    print(dir(raisins)[:3])
    # ['_NonBlank#0', '_Quantity_5#0', '_Quantity_5#1']

