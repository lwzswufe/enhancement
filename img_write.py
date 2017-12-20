# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import os
from PIL import Image, ImageFont, ImageDraw


'''
text(xy, text, fill=None, font=None, anchor=None, *args, **kwargs) method of PIL.ImageDraw.ImageDraw instance
指定字体和颜色（RGB）
draw.text( (0，100), u’He acknowledged his faults.', font=font_en,fill=(0,0,0))
'''


def demo(context, idx=0, default_img='D:\\Cache\\message.png', output_path='D:\\Cache\\img_cache\\czt_'):
    ttfont = ImageFont.truetype(font=r'C:\Windows\Fonts\simkai.ttf', size=30)
    im = Image.open(default_img)
    draw = ImageDraw.Draw(im)
    draw.text(xy=(38, 44), text=context, font=ttfont, fill=(255, 0, 0))
    img_name = output_path + str(idx).zfill(3) + '.png'
    im.save(img_name)


if __name__ == '__main__':
    demo('11:14:21 大单买入 科达洁能\n代码 600499 价格 10.98 \n', idx=0)
    demo('11:14:21 大单买入 埃杜阿多\n代码 999888 价格 10.98 \n', idx=1)

