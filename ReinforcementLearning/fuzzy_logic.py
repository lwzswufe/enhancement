# author='lwz'
# coding:utf-8
import numpy as np
'''
模糊推理
'''

def o(a, b):
    row_n = a.shape[0]
    b = b.T
    col_n = b.shape[0]
    c = np.zeros([row_n, col_n])
    for i in range(row_n):
        for j in range(col_n):
            c[i, j] = np.max(np.min([a[i, :], b[j, :]], axis=0))
    return c

def example():
    a = [[0.1, 0.3, 0.5, 0.7],
         [0.4, 0.2, 0.8, 0.9],
         [0.6, 0.8, 0.3, 0.2]]
    a = np.array(a)
    print("x >> y:\n", a)
    b = [[0.9, 0.1],
         [0.2, 0.3],
         [0.5, 0.6],
         [0.7, 0.2]]
    b = np.array(b)
    print("y >> z:\n", b)
    print("x >> z:\n", o(a, b))


if __name__ == '__main__':
    example()