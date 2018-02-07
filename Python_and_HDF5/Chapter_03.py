# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import h5py
import numpy as np
import os
import timeit
import time


fn = "tetsfile.hdf5"
fn1 = 'big1.hdf5'
fn2 = 'big2.hdf5'

for fname in [fn, fn1, fn2]:
    if os.path.exists(fname):
        os.remove(fname)

f = h5py.File(fn)
arr = np.ones((5, 2))
f["my dataset"] = arr
dset = f["my dataset"]
print(dset)
print(dset.size)
print("数据类型dtype: {}\n数据维度shape:{}".format(dset.dtype, dset.shape))
print("文件大小:{}".format(os.path.getsize(fn)))

print("创建空数据集")
dset = f.create_dataset("test1", (10, 10))
print(dset)
print("默认储存精度单精度f4  默认计算精度双精度F8")
dset = f.create_dataset("test2", (10, 10), dtype=np.complex64)
print(dset)

print("显示指定数据数据类型来节省空间")
bigdata = np.ones((100, 1000))
print("生成数据 dtype={} shape={}".format(bigdata.dtype, bigdata.shape))
with h5py.File('big1.hdf5', 'w') as f1:
    f1['big'] = bigdata

with h5py.File('big2.hdf5', 'w') as f2:
    f2.create_dataset('big', data=bigdata, dtype=np.float32)

f1 = h5py.File(fn1)
f2 = h5py.File(fn2)
print("数据类型dtype: {}\n数据维度shape:{}\n文件大小:{}".
      format(f1['big'].dtype, f1['big'].shape, os.path.getsize(fn1)))
print("数据类型dtype: {}\n数据维度shape:{}\n文件大小:{}".
      format(f2['big'].dtype, f2['big'].shape, os.path.getsize(fn2)))

print("使用read_direct转写数据格式")
dset = f2['big']
big_out = np.empty((100, 1000), dtype=np.float64)
dset.read_direct(big_out)

with dset.astype("float64"):
    astype_out = dset[:, :]

with dset.astype("float64"):
    astype_out2 = dset

print("原始数据：\n数据类型dtype: {}\n数据维度shape:{}".format(dset.dtype, dset.shape))
print("读取数据1：\n数据类型dtype: {}\n数据维度shape:{}".format(big_out.dtype, big_out.shape))
print("读取数据2：\n数据类型dtype: {}\n数据维度shape:{}".format(astype_out.dtype, astype_out.shape))
print("读取数据3：\n数据类型dtype: {}\n数据维度shape:{}".format(astype_out2.dtype, astype_out2.shape))

print("利用create_dataset改变数据维度 reshape")
f2.create_dataset("big2", data=f2['big'], shape=(1000, 100))
dset = f2['big']
print("原始数据：\n数据类型dtype: {}\n数据维度shape:{}".format(dset.dtype, dset.shape))

dset1 = f.create_dataset('empty', (2, 2), dtype=np.int32)
print("默认空值为0", dset1.value)
print("默认填充值:", dset1.fillvalue)
dset2 = f.create_dataset('filled', (2, 2), dtype=np.int32, fillvalue=42)
print("更改默认空值为42", dset2.value)
print("默认填充值:", dset2.fillvalue)

dset = f2['big']
out = dset[0:10, 20:70]
print("数据切片 dset[0:10, 20:70]", out.shape)

dset = f2['big']
t1 = time.time()
for ix in range(100):
    for iy in range(1000):
        val = dset[ix, iy] # Read one element
        if val < 0:
            dset[ix, iy] = 0  # Clip to 0 if needed

print("每次读取一个元素用时{:.4f}s".format(time.time() - t1))

dset = f2['big']
t2 = time.time()
# Check for negative values and clip to 0
for ix in range(100):
    val = dset[ix, :]  # Read one row
    val[val < 0] = 0
    dset[ix, :] = val
print("每次读取一行元素用时{:.4f}s".format(time.time() - t2))

dset = f2['big']
t3 = time.time()
# Check for negative values and clip to 0
val = dset[:, :]
val[val < 0] = 0
dset[:, :] = val
print("一次读取所有元素用时{:.4f}s".format(time.time() - t3))

print(dset1[()])
print('数据广播 dset[:, :]=dset[0, :]')

print("maxshape 不可改变 None表示无上限 shape可以改变")
dset1 = f.create_dataset('big', (1, 7), maxshape=(None, 7))
print(dset1.value)
dset1.resize((dset1.shape[0] + 1, 7))
dset1[-1, :] = -1
print(dset1.value)

for fname in [fn, fn1, fn2]:
    if os.path.exists(fname):
        os.remove(fname)

