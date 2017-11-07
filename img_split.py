# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import os
from PIL import Image


def demo():
    name1 = "001.jpg"
    name2 = "002.jpg"
    im = Image.open(name1)
    print(im.height, im.width)
    im2 = im.crop((0, 0, int(im.width / 2), int(im.height / 2)))
    # left, upper, right, and lower
    im2.save(name2)


def main(file_path="D:\\Code\\Code\\", rewrite=False):
    flag = 0
    for root, dirs, files in os.walk(file_path):
        for fn in files:
            suffix = fn[-4:]
            if suffix == '.jpg' or suffix == '.png':
                flag += 1
                divide_into_2(root + '\\' + fn)


def divide_into_2(fn):
    if fn[-6] == "_":
        return

    im = Image.open(fn)
    if im.width < im.height:
        return

    im_1 = im.crop((0, 0, round(im.width / 2, 0), im.height))
    im_2 = im.crop((round(im.width / 2, 0), 0, im.width, im.height))

    name_1 = fn[:-4] + '_1' + fn[-4:]
    name_2 = fn[:-4] + '_2' + fn[-4:]
    im_1.save(name_1)
    im_2.save(name_2)


if __name__ == '__main__':
    main(file_path="D:\\360安全浏览器下载")




