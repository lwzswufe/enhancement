# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
from collections import namedtuple


Customer = namedtuple('Customer', 'name fidelity')
promos = []


class LineItem:  # 购物车
	def __init__(self, product, quantity, price):
		self.product = product
		self.quantity = quantity
		self.price = price

	def total(self):
		return self.price * self.quantity


class Order:  # the Context
	def __init__(self, customer, cart, promotion=None):
		self.customer = customer
		self.cart = list(cart)
		self.promotion = promotion

	def total(self):
		if not hasattr(self, '__total'):
			self.__total = sum(item.total() for item in self.cart)
		return self.__total

	def due(self):
		if self.promotion is None:
			discount = best_promo(self)
		else:
			discount = self.promotion(self)
		return self.total() - discount

	def __repr__(self):
		fmt = '<订单 总计: {:.2f} 折扣后: {:.2f}>'
		return fmt.format(self.total(), self.due())


def best_promo(order):
	"""Select best discount available
	"""
	return max(promo(order) for promo in promos)


def promotion(promo_func):
	promos.append(promo_func)
	print(promos)
	return promo_func


@promotion  # 装饰器 相当于promotion(fidelity_promo)
def fidelity_promo(order):
	"""5% discount for customers with 1000 or more fidelity points"""
	return order.total() * .05 if order.customer.fidelity >= 1000 else 0


@promotion
def bulk_item_promo(order):
	"""10% discount for each LineItem with 20 or more units"""
	discount = 0
	for item in order.cart:
		if item.quantity >= 20:
			discount += item.total() * .1
	return discount


@promotion
def large_order_promo(order):
	"""7% discount for orders with 10 or more distinct items"""
	distinct_items = {item.product for item in order.cart}
	if len(distinct_items) >= 10:
		return order.total() * .07
	return 0


def make_averager():
	series = []  # 闭包延伸到函数作用域之外 子函数可以使用该变量
	count = 0
	total = 0

	def averager_1(new_value):
		series.append(new_value)  # 我们没有为series 赋值 所以series仍然是自由变量 而非局部变量
		total = sum(series)
		return total/len(series)

	def averager_2(new_value):
		nonlocal count, total  # 不可变数据类型的闭包需要用nonlocal声明
		count += 1
		total += new_value
		return total/count

	return averager_1, averager_2


if __name__ == "__main__":
	joe = Customer('John Doe', 0)
	ann = Customer('Ann Smith', 1100)
	cart = [LineItem('banana', 4, .5),
			LineItem('apple', 10, 1.5),
			LineItem('watermellon', 5, 5.0)]
	print(Order(joe, cart, fidelity_promo))
	print(Order(ann, cart, fidelity_promo))
	banana_cart = [LineItem('banana', 30, .5), LineItem('apple', 10, 1.5)]
	print(Order(joe, banana_cart, bulk_item_promo))

	avg_1, avg_2 = make_averager()
	print("avg_1: ", avg_1(7), "avg_2: ", avg_2(7))
	print("avg_1: ", avg_1(8), "avg_2: ", avg_2(8))
	print("avg_1: ", avg_1(15), "avg_2: ", avg_2(15))
	print("series" in locals().keys())  # 判断变量是否存在
	print("series" in globals().keys())
