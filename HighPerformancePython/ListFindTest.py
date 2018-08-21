# author='lwz'
# coding:utf-8
'''
查找效率测试
使用try 方法的效率会低68% 1.12us 对1.89us
'''

import time


def find_1(vol, vols):
    if vol in vols[1:]:
        return vols[1:].index(vol)
    else:
        return -1


def find_2(vol, vols):
    try:
        idx = vols[1:].index(vol)
    except ValueError:
        return -1
    else:
        return idx


def main():
    s = '7543|52|9|10|10|18|10|429|20|75|100|7100|73|50|25|272|102|119|175|10|84|139|1|1|108|49|90|21|1427|1|1|7|2|6|31|8|584|95|1|88|8|10|33|252|6|427|1363|3|30|16'
    vols = [int(x) for x in s.split('|')]
    N = 10000
    st_time = time.time()
    for i in range(N):
        find_1(i, vols)
    used_time = time.time() - st_time
    print("time used{:.3f}us".format(used_time / N * 10**6))

    st_time = time.time()
    for i in range(N):
        find_2(i, vols)
    used_time = time.time() - st_time
    print("time used{:.3f}us".format(used_time / N * 10**6))


if __name__ == "__main__":
    main()