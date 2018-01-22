# author='lwz'
# coding:utf-8
from numexpr import evaluate
import numpy as np
import time
import ctypes


def array_init(size=100):
    st = -1.8
    ed = 1.8
    step = (ed - st) / (size - 1)
    z = np.arange(st, ed, step, dtype=np.complex)
    z += z * np.complex(0, 1)
    return z


def julia(size=100, times=10):
    z = array_init(size)
    for i in range(times):
        z = z * z + 0.2


def numexpy_julia(size, times=10):
    z = array_init(size)
    for i in range(times):
        evaluate("z * z + 0.2", out=z)


def main():
    print("使用numexpr编译代码 提高运算速度")
    for size in [100, 1000, 10000, 100000, 1000000]:
        for f in [julia, numexpy_julia]:
            st = time.time()
            f(size, times=1000)
            print("def {:>14} with size {:<8} used {:.4f}s".format(f.__name__, size, time.time() - st))


if __name__ == "__main__":
    main()