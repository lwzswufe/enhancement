# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import copy


class Bus:
	def __init__(self, passengers=None):
		if passengers is None:
			self.passengers = []
		else:
			self.passengers = list(passengers)

	def pick(self, name):
		self.passengers.append(name)

	def drop(self, name):
		self.passengers.remove(name)


if __name__ == "__main__":
	bus1 = Bus(['Alice', 'Bill', 'Claire', 'David'])
	bus2 = copy.copy(bus1)  # 复制引用
	bus3 = copy.deepcopy(bus1)  # 复制值
	print(id(bus1), id(bus2), id(bus3))
	print(bus1.passengers)  # bus1 bus2 共享一个对象
	print(bus2.passengers)
	bus1.drop('Bill')
	print(bus1.passengers)
	print(bus2.passengers)
	print(id(bus1.passengers), id(bus2.passengers), id(bus3.passengers))
	print(bus3.passengers)