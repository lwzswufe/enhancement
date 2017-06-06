# author='lwz'
# coding:utf-8
# !/usr/bin/env python3


class A:
    def ping(self):
        print('A_ping:', self)


class B(A):
    def pong(self):
        print('B_pong:', self)


class C(A):
    def pong(self):
        print('C_PONG:', self)


class D(B, C):

    def ping(self):
        super().ping()
        print('D_post-ping:', self)

    def pingpong(self):
        self.ping()
        super().ping()  # A.ping
        self.pong()     # B.pong
        super().pong()  # B.pong
        C.pong(self)    # C.pong


if __name__ == "__main__":
    d = D()
    print(d.pong)
    print(C.pong(d))
    print(d.pingpong())
    c = C()
    print(c.pong())
    print(D.__mro__)  # 显示D的父类顺序
