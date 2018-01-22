# author='lwz'
# coding:utf-8
import time
from functools import wraps
# from guppy import h5py


'''
初始版 计算julia集合 测试程序速度
框架中的一些函数添加自定义的decorator，添加后由于函数名和函数的doc发生了改变
，对测试结果有一些影响。所以，Python的functools包中提供了一个叫wraps的decorator
来消除这样的副作用。写一个decorator的时候，最好在实现之前加上functools的wrap，
它能保留原有函数的名称和docstring
'''
# hasattr(__builtins__, 'profile') 判断命名空间__builtins__里有没有profile
# '__builtin__' not in dir() 针对nosetest
'''
nosetests参数说明：

-v:查看测试详细信息
-s:显示脚本print信息,默认是print的信息是不输出的
nose会查找脚本中 test_命名的函数和Test_命名的类
运行测试脚本时,首先会运行脚本func级别的setUp()函数,
这时候初始化web.py的app
之后会执行class级别的setUp(self)函数,
这时候初始self的app变量为之前初始化的app

#这时候类的__init__()函数是不起作用的
更详细的测试用例可以在test函数中编写,
数据库之类的初始化可以再setUp()函数中编写
'''
if '__builtin__' not in dir() or not hasattr(__builtins__, 'profile'):
    print('我们在命名空间里没有找到 @profile 于是自建了一个no-op的profile函数供@profile修饰符调用')
    def profile(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner

# hp = h5py()
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

    if __name__ == '__main__' and False:
        pass
        # h = hp.heap()
        # print(h)

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
@profile
# line_profiler 会记录分析@profile装饰的函数 使用这个会显著的降低程序运行总时间
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


