# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import os
import codecs


def object_change(old_name="para", new_name="barsize",
                  file_path="D:\\Code\\Code\\MATLABCode\\wztoolbox\\Trade_v3", file_end=".m"):
    # Path to the folder with files to convert
    # 批量修改程序对象名称
    end_num = len(file_end)
    for root, dirs, files in os.walk(file_path):
        for fn in files:
            if fn[-end_num:] == file_end:  # Specify type of the files
                fname = os.path.join(root, fn)
                content = read_file(fname, 'gbk')
                content = content.replace(old_name, new_name)
                write_file(fname, content, 'gbk')


def read_file(filename, encode="utf-8"):
    with codecs.open(filename, "r", encoding=encode) as f:
        content = f.read()
        f.close()
        return content


def write_file(filename, content, encode="gbk"):
    with codecs.open(filename, "w", encoding=encode) as f:
        f.write(content)
        f.close()


if __name__ == '__main__':
    object_change(old_name="[Day, Time, Open, High, Low, Close, Vol, status] = CycleChange_v3(bars, original_barsize,  InitialSet.barsize);",
                  new_name="[Day, Time, Open, High, Low, Close, Vol, status] = CycleChange_v3(bars, InitialSet.original_barsize,  InitialSet.barsize);",
                  file_path="D:\\Code\\Code\\MATLABCode\\strategy")
