# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
from PIL import Image, ImageFont, ImageDraw


'''
text(xy, text, fill=None, font=None, anchor=None, *args, **kwargs) method of PIL.ImageDraw.ImageDraw instance
指定字体和颜色（RGB）
draw.text( (0，100), u’He acknowledged his faults.', font=font_en,fill=(0,0,0))
'''


class img_generator(object):
    def __init__(self, config, img_idx=0):
        self.font = ImageFont.truetype(font=config['font_path'], size=config['size'])
        self.xy = tuple(config['xy'])
        self.template_img = Image.open(config['template_img'])
        self.color = tuple(config['color'])  # 0~255 RGB
        self.img_idx = img_idx
        self.output_path = config['output_path']
        self.img_type = config['template_img'][-4:]
        self.line_space = 0.5 * config['size']
        self.xy2 = (config['xy'][0], config['xy'][1] + self.line_space + config['size'])
        print("img size: ", self.template_img.height, self.template_img.width)

    def get_img(self, context):
        self.img_idx += 1
        im = self.template_img.copy()
        draw = ImageDraw.Draw(im)
        t1, t2 = self.context_split(context)
        if len(t2) == 0:
            print(t1)
            return ''

        draw.text(xy=self.xy,  text=t1, font=self.font, fill=self.color)
        draw.text(xy=self.xy2, text=t2, font=self.font, fill=self.color)
        fn = self.get_img_filename()
        im.save(fn)
        return '@img@' + fn

    def context_split(self, context='1 2 3'):
        mid = context.find('代码')
        if mid < 0:
            return 'we do not find "代码"', ''
        else:
            return context[:mid], context[mid:]

    def get_img_filename(self):
        return self.output_path + str(self.img_idx).zfill(3) + self.img_type

    def get_imgs(self, contexts=['a', 'b']):
        imgs = list()
        for context in contexts:
            imgs.append(self.get_img(context))
        return  imgs


if __name__ == '__main__':
    config = {'font_path': r'C:\Windows\Fonts\simkai.ttf', 'size': 36, 'xy': [44, 55],
              'template_img': 'D:\\Cache\\img_cache\\message.jpg', 'color': [0, 0, 0],
              'output_path': 'D:\\Cache\\img_cache\\czt_', 'Line Spacing': None}
    ig = img_generator(config, img_idx=0)

    ig.get_img('11:14:21 大单买入 科达洁能 代码 600499 价格 10.98')
    ig.get_imgs(['11:14:21 大单买入 科达洁能 代码 600499 价格 10.98',
                 '11:14:21 大单买入 奥运会上 代码 990499 价格 10.98'])

