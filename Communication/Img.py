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


class img_generator(object):
    def __init__(self, config, img_idx=0):
        self.font = ImageFont.truetype(font=config['font_path'], size=config['size'])
        self.xy = config['xy']
        self.template_img = Image.open(config['template_img'])
        self.color = config['color']  # 0~255 RGB
        self.img_idx = img_idx
        self.output_path = config['output_path']
        self.img_type = config['template_img'][-4:]
        print("img size: ", self.template_img.height, self.template_img.width)

    def get_img(self, context):
        self.img_idx += 1
        im = self.template_img.copy()
        draw = ImageDraw.Draw(im)
        draw.text(xy=self.xy, text=context, font=self.font, fill=self.color)
        fn = self.get_img_filename()
        im.save(fn)
        return '@img@' + fn

    def get_img_filename(self):
        return self.output_path + str(self.img_idx).zfill(3) + self.img_type

    def get_imgs(self, contexts=['a', 'b']):
        imgs = list()
        for context in contexts:
            imgs.append(self.get_img(context))
        print(imgs)


if __name__ == '__main__':
    config = {'font_path': r'C:\Windows\Fonts\simkai.ttf', 'size': 30, 'xy': (38, 44),
              'template_img': 'D:\\Cache\\message.png', 'color': (255, 127, 0),
              'output_path': 'D:\\Cache\\img_cache\\czt_'}
    ig = img_generator(config, img_idx=0)

    ig.get_img('11:14:21 大单买入 科达洁能\n代码 600499 价格 10.98 \n')
    ig.get_imgs(['11:14:21 大单买入 科达洁能\n代码 600499 价格 10.98 \n',
                 '11:14:21 大单买入 奥运会上\n代码 990499 价格 10.98 \n'])

