# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import collections
from random import shuffle


Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck2(collections.MutableSequence):
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, position, value):  # 支持随机抽取方法所必需
        self._cards[position] = value

    def __delitem__(self, position):  # 继承MutableSequence必须实现该方法
        del self._cards[position]

    def insert(self, position, value):  # 继承MutableSequence必须实现该方法
        self._cards.insert(position, value)


if __name__ == "__main__":
    deck = FrenchDeck2()
    print(deck)
    print(deck[1:7])
    print(shuffle(deck))  # 打乱牌组
    print(deck[1:7])
