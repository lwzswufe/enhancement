# author='scarlett'
# coding:utf-8
import time
from functools import wraps
'''
初始版
计算julia集合 测试程序速度
框架中的一些函数添加自定义的decorator，添加后由于函数名和函数的doc发生了改变
，对测试结果有一些影响。所以，Python的functools包中提供了一个叫wraps的decorator
来消除这样的副作用。写一个decorator的时候，最好在实现之前加上functools的wrap，
它能保留原有函数的名称和docstring
'''

x1, x2, y1, y2 = -1.8, 1.8, -1.8, 1.8
c_real, c_imag = -0.62772, -0.42193
# julia集合的复数点


def calc_pure_python(desired_width, max_iterations):
    '''
    :param desired_width: 像素
    :param max_iterations: 最大迭代步数
    :return: None
    '''
    x_step = (float(x2 - x1)) / float(desired_width)
    y_step = (float(y1 - y2)) / float(desired_width)
    x = []
    y = []
    ycoord = y2
    while ycoord > y1:
        y.append(ycoord)
        ycoord += y_step
    xcoord = x1
    while xcoord < x2:
        x.append(xcoord)
        xcoord += x_step

    zs = []
    cs = []

    for ycoord in y:
        for xcoord in x:
            zs.append(complex(xcoord, ycoord))
            cs.append(complex(c_real, c_imag))

    print("Length of x:", len(x))
    print("total elements", len(zs))
    start_time = time.time()
    output = calculate_z_serial_purepython(max_iterations, zs, cs)
    end_time = time.time()
    secs = end_time - start_time
    print("{} took {:.4f}secs".format(calculate_z_serial_purepython.__name__, secs))

    # assert sum(output) == 33219980


def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t_st = time.time()
        print("装饰器1调用函数开始")
        result = fn(*args, **kwargs)
        time.sleep(0.1)
        print("装饰器1调用函数结束")
        t_ed = time.time()
        print("@timefn: {} took {:.4f}s ".format(fn.__name__, t_ed-t_st))
        return result
    return measure_time


def timefn_without_warps(fn):
    def measure_time_without_warps(*args, **kwargs):
        t_st = time.time()
        print("装饰器2调用函数开始")
        result = fn(*args, **kwargs)
        print("装饰器2调用函数结束")
        t_ed = time.time()
        print("@timefn: {} took {:.4f}s ".format(fn.__name__, t_ed-t_st))
        return result
    return measure_time_without_warps


@timefn  # 实际上的调用是timefn(calculate_z_serial_purepython(*args, **kwargs))
@timefn_without_warps  # timefn_without_warps(timefn(calculate_z_serial_purepython))
# 装饰器1(装饰器2(被装饰函数))
def calculate_z_serial_purepython(maxiter, zs, cs):
    '''
    子程序 迭代计算f(z) = z*z + c 是否收敛
    '''
    output = [0] * len(zs)
    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]
        while abs(z) < 2 and n < maxiter:
            z = z * z + c
            n += 1
        output[i] = n
    return output


if __name__ == '__main__':
    calc_pure_python(desired_width=1000, max_iterations=300)
