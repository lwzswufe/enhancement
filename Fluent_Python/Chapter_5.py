# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import random
from inspect import signature
from functools import partial


def factorial(n):
	'''return n!'''
	return 1 if n < 2 else n * factorial(n - 1)


class BingoCage:

	def __init__(self, items):
		self._items = list(items)
		random.shuffle(self._items)

	def pick(self):
		try:
			return self._items.pop()
		except IndexError:
			raise LookupError('pick from empty BingoCage')
		# 抛出异常并设定错误信息

	def __call__(self):
		return self.pick()


def tag(name, *content, cls=None, **attrs):
	"""Generate one or more HTML tags"""
	# **attrs 捕获多余的参数
	if cls is not None:
		attrs['class'] = cls
	if attrs:
		attr_str = ''.join(' %s="%s"' % (attr, value)
						   for attr, value in sorted(attrs.items()))
	else:
		attr_str = ''
	if content:
		return '\n'.join('<%s%s>%s</%s>' %(name, attr_str, c, name) for c in content)
	else:
		return '<%s%s />' % (name, attr_str)


def clip(text:str, max_len:'int > 0'=80) -> str:
	"""Return text clipped at the last space before or after max_len
	"""
	end = None
	if len(text) > max_len:
		space_before = text.rfind(' ', 0, max_len)
	if space_before >= 0:
		end = space_before
	else:
		space_after = text.rfind(' ', max_len)
	if space_after >= 0:
		end = space_after
	if end is None:  # no spaces were found
		end = len(text)
	return text[:end].rstrip()


if __name__ == "__main__":
	print(list(map(factorial, range(11))))
	bingo = BingoCage(range(3))
	print(bingo.pick())
	print(bingo)
	print(callable(bingo))

	print(tag('br'))
	print(tag('p', 'hello'))
	print(tag('p', 'hello', 'world'))
	print(tag('p', 'hello', id=33))
	print(tag('p', 'hello', 'world', cls='sidebar'))
	print(tag(content='testing', name="img"))

	freezing_tag = partial(tag, cls='freezing')  # 创建冻结参数的函数
	print(freezing_tag('p', 'hello'))

	freezing_tag = partial(tag, 'freezing')  # 创建冻结参数的函数
	print(freezing_tag('p', 'hello'))

	print(tag.__defaults__)  # 获取参数默认值
	print(tag.__code__.co_varnames)  # 获取参数名
	print(tag.__code__.co_argcount)  # 获取参数数量 不含 * **开头的变长函数
	sig = signature(tag)
	for name, param in sig.parameters.items():
		print(param.kind, ":", name, "=", param.default)

	print(clip.__annotations__)  # 获取函数注解
