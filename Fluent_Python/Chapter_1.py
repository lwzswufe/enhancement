# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
# 数据结构
import collections
from math import hypot

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
	ranks = [str(n) for n in range(2, 11)] + list('JQKA')
	suits = ['spades', 'diamonds', 'clubs', 'hearts']

	def __init__(self):
		self._cards = [Card(rank, suit) for suit in self.suits
		                                for rank in self.ranks]

	def __len__(self):
		return len(self._cards)

	def __getitem__(self, position):
		return self._cards[position]


class Vector:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def __repr__(self):      # 字符表达式
		return "Vector(%r, %r)" % (self.x, self.y)

	def __abs__(self):       # 求模
		return hypot(self.x, self.y)

	def __bool__(self):      # 求布尔值
		return bool(abs(self))

	def __add__(self, other):  # 加法
		x = self.x + other.x
		y = self.y + other.y
		return Vector(x, y)

	def __mul__(self, scalar):  # 乘法
		return Vector(scalar * self.x, scalar * self.y)

if __name__ == "__main__":
	deck = FrenchDeck()
	for card in deck:
		if card.rank == 'A':
			print(card)
	print(len(deck))
	print(Vector(1, 2) * 3)
	print(Vector(3, 4) + Vector(1, 1))