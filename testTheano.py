# -*- coding: utf-8 -*-

from theano import function, config, shared, sandbox
import theano.tensor as T
import numpy
import time


t1 = time.time()
vlen = 10 * 30 * 768  # 10 x #cores x # threads per core
iters = 1000

rng = numpy.random.RandomState(22)
x = shared(numpy.asarray(rng.rand(vlen), config.floatX))
# floatX: 'float64', 'float32', or 'float16'定义数据类型
f = function([], T.exp(x))
# defines theano.function; we can use it like:
# zz = T.dscalar()
# xx = T.dscalar()
# ff = function([xx, zz], T.exp(xx) + zz)
# ff(0, 2) = 3;ff(0, 2) = exp(0) + 2 = 3
print(f.maker.fgraph.toposort())
t0 = time.time()
for i in range(iters):
    r = f()

print('Looping %d times took' % iters, t0 - t1, 'seconds')
print('Result is' + str(r))
if numpy.any([isinstance(x.op, T.Elemwise) for x in f.maker.fgraph.toposort()]):
    print('Used the cpu')
else:
    print('Used the gpu')
print(time.time() - t1)