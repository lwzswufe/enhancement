# author='lwz'
# coding:utf-8
import time
import math


class A(object):
    def __init__(self, prime):
        self.prime_num = prime

    @property
    def value(self):
        print('start calculation')
        for i in range(2, int(math.sqrt(self.prime_num))):
            if self.prime_num % i == 0:
                return False, i
        else:
            return True, 0


if __name__ == '__main__':
    a = A(1234567891234571)
    a.prime_num = 1236835000487
    print('调用特性的时候才会触发方法, 修改其他值并不会触发方法')
    print(a.value)


