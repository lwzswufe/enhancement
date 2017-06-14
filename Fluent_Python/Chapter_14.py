# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence3:

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):  # <1>
        return SentenceIterator(self.words)  # 实例化 并返回一个迭代器


class SentenceIterator:  # 迭代器 实现了next与iter方法

    def __init__(self, words):
        self.words = words  # <3>
        self.index = 0  # <4>

    def __next__(self):
        try:
            word = self.words[self.index]  # <5>
        except IndexError:
            raise StopIteration()  # <6>
        self.index += 1  # <7>
        return word  # <8>

    def __iter__(self):  # <9>
        return self


class Sentence4:

    def __init__(self, text):
        self.text = text  # <1>

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for match in RE_WORD.finditer(self.text):  # <2>
            yield match.group()  # <3>
# 包涵关键字 yield 该函数就是生成器函数
# 返回 生成器


class Sentence5:

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        return (match.group() for match in RE_WORD.finditer(self.text))
# 生成器表达式
# END SENTENCE_GENEXP


def gen():
    for i in range(7):
        print('iter ' + str(i))
        yield str(i)


if __name__ == "__main__":
    C = Sentence3('i see you')
    iters = iter(C)
    print(iters)
    print('next ', next(iters))
    for it in iters:
        print('for ', it)
    C = Sentence4('i see you')
    for it in C:
        print(it)
    C = Sentence5('i see you')
    for it in C:
        print(it)
    g = gen()  # 返回生成器 但是还没有计算结果
    print('start')
    for i in range(7):
        print('value ' + next(g))  # 每一次迭代 都是next调用生成器生成结果
