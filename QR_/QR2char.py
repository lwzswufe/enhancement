# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
from PIL import Image
import numpy as np


# 将图片二维码转化为文字二维码


def get_gray_img(img):
    gray = np.sum(np.array(img), axis=2)
    height, width = gray.shape
    sum_row = np.sum(gray, axis=1)
    gray = gray[sum_row < width*254*3, :]
    height, width = gray.shape
    sum_col = np.sum(gray, axis=0)
    gray = gray[:, sum_col < height*254*3]
    gray[gray < 128 * 3] = 0
    gray[gray >= 128 * 3] = 255
    return gray


def get_pixel_size(gray):
    a = set(np.argmax(gray, axis=1))
    a.remove(0)
    pixel_hieght = min(a)

    b = set(np.argmax(gray, axis=0))
    b.remove(0)
    pixel_wieght = min(b)
    return pixel_hieght, pixel_wieght


def get_qrcode(gray):
    h_g, w_g = gray.shape
    h_p, w_p = get_pixel_size(gray)
    assert h_g % h_p == 0
    assert w_g % w_p == 0

    height = int(h_g/h_p)
    width = int(w_g/w_p)
    code = ''

    for y in range(height):

        for x in range(width):
            cell = gray[y*h_p:y*h_p + h_p, x*w_p:x*w_p + w_p]
            if np.mean(cell) < 128:
                code += '▇'
                #code += '繁,'
            else:
                code += '　'
        code += '\n'

    return code


def write_code(code, fn="qr.txt"):
    with open(fn, 'w') as f:
        f.write(code)


def main(img_fn='QR01.jpg'):
    im = Image.open(img_fn)
    gray = get_gray_img(im)
    code = get_qrcode(gray)
    write_code(code)


if __name__ == '__main__':
   main()
