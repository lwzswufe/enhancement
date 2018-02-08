# author='lwz'
# coding:utf-8
import h5py
import os


fn = "Groups.hdf5"
fn2 = "Groups2.hdf5"
print("创建子数据组。。。")
f = h5py.File(fn, 'w')
subgroup = f.create_group("SubGroup")
print(subgroup)
print("子数据组名称", subgroup.name)

subsubgroup = subgroup.create_group("SubSubGroup")
print("子子数据组名称", subsubgroup.name)

out = f.create_group('/some/big/path')
print("自动创建目录:", out)

print("测试存在性:  if subgroup_name in group_name:")
if "SubSubGroup" in subgroup:
    print("SubSubGroup in subgroup")

grpy = f.create_group('x')
f['y'] = grpy

print("重名：", grpy.name)

print("删除链接  del f['x'] ")
del f['x']

print("唯一名字：", grpy.name)

grp = f.create_group("my_group")
dset = grp.create_dataset('dataset', (100, ))
f['hardlink'] = dset
print("硬链接: 链接名字-->> 文件中对象 f['hardlink'] = dset")
grp.move('dataset', 'new_name')
print("数据组变更名称：grp.move('dataset', 'new_name') ")
print(f['hardlink'] == grp['new_name'])

grp.move('new_name', 'dataset')
# 改回名称
f['softlink'] = h5py.SoftLink("/my_group/dataset")
print("软链接: 链接名字-->> f['softlink'] = h5py.SoftLink('/my_group/dataset')")
print(f['softlink'] == grp['dataset'])

print("使用get获取对象类型 ")
for name in f:
    try:
        print("Name:{:<8}, Type:{}".format(name, f.get(name, getclass=True)))
    except KeyError:
        print("Name:{}, No found".format(name))

print("使用get获取对象地址 ")
for name in f:
    try:
        print("Name:{:<8}, Link:{}".format(name, f.get(name, getlink=True)))
    except KeyError:
        print("Name:{}, No found".format(name))


def printname(name):
    print(name)

print("visitor 遍历模式 遍历名称 f.visit(回调函数) ")
f.visit(printname)


def printobj2(name, obj):
    print(name, obj)
    # 如果返回任何值都会终止进程

print("visitor 遍历模式 遍历对象 f.visititems(回调函数) ")
grp.visititems(printobj2)

f.create_dataset('my_group/apples', (100,))
f.copy('my_group', 'my_group2')
print("复制对象（包含子文件） f.copy('my_group', 'my_group2')")
print(f['my_group'] == f['my_group2'])
f.visit(printname)

f.close()
for fname in [fn]:
    if os.path.exists(fname):
        os.remove(fname)
