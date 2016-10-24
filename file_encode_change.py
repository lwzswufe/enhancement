# author='lwz'
# coding:gbk
# !/usr/bin/env python3
import os
import codecs


def encode_change(read_codes="utf-8", write_codes="gbk",
                  file_path="D:\\Code\\Code\\", file_end=".m"):
    # Path to the folder with files to convert
    end_num = len(file_end)
    for root, dirs, files in os.walk(file_path):
        for fn in files:
            if fn[-end_num:] == file_end:  # Specify type of the files
                fname = os.path.join(root, fn)
                content = read_file(fname, read_codes)
                write_file(fname, content, write_codes)


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
    encode_change(read_codes="utf-8", write_codes="gbk",
                  file_path="D:\\Code\\Code\\data\\",
                  file_end=".m")