# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import abc


class Quantity_3:  # 描述符类
    name = 'quantity'

    def __init__(self, storage_name):
        self.storage_name = storage_name

    def __set__(self, instance, value):
        print("self 传入描述符类:", self.name, "instance传入托管类:", instance.name)
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            raise ValueError('value must be > 0')


class LineItem_3:  # 托管类
    name = 'lineitem3'
    weight = Quantity_3('weight')
    price = Quantity_3('price')

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


class Quantity_4:
    __counter = 0
    __flag = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        # self.storage_name = ' '
        print("不同的storage_name确保每个属性映射到不同的托管类属性中")
        cls.__counter += 1
        self.__flag += 1

        if cls.__counter == 1:
            print("cls 属性变更会影响 self, cls={}, self={}".format(cls.__counter, self.__counter))
            print("self属性变更不会影响cls, cls={}, self={}".format(cls.__flag, self.__flag))
            print("cls.__name__:  {}".format(cls.__name__))
            print("实例(self) has no attribute '__name__")
            print(self.storage_name)

    def __get__(self, instance, owner):
        if instance is None:
            print("we donot have such a attribute")
        else:
            print(owner)
            return getattr(instance, self.storage_name)  # 将属性映射到不同的托管类属性中

    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.storage_name, value)
        else:
            raise ValueError('value must be > 0')


class LineItem_4:
    weight = Quantity_4()
    price = Quantity_4()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        print("weight: {}\nprice: {}".format(self.weight, self.price))
        return self.weight * self.price


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


class Quantity_5(Validated):
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


class LineItem_5:
    description = NonBlank()
    weight = Quantity_5()
    price = Quantity_5()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

if __name__ == "__main__":
    walnuts = LineItem_3('walnuts', 1, 10.00)

    walnut_4 = LineItem_4('walnuts', 3, 10.00)
    print(walnut_4.subtotal())

    walnut_5 = LineItem_5('walnuts', 3, 10.00)
    print(walnut_5.subtotal())
    print(Quantity_5.__mro__)
    print(dir(walnut_5)[:3])