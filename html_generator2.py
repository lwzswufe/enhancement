# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import os


def main(file_path="D:\\Code\\Code\\", rewrite=False):
    traget_dir = ''
    target_root = ''
    file_lists = list()
    sub_dir_lists = list()
    for root, dirs, files in os.walk(file_path):
        dir_name, sub_dir_name, idx, root = get_dir_name(root)

        if traget_dir != dir_name:
            html_ = Html(traget_dir, target_root, rewrite)
            html_.add_files(sub_dir_lists, file_lists)
            sub_dir_lists = list()
            file_lists = list()
            traget_dir = dir_name
            target_root = root
            del html_

        file_lists.insert(idx, files)   # 文件列表
        sub_dir_lists.insert(idx, sub_dir_name)  # 子文件夹列表

    html_ = Html(traget_dir, target_root, rewrite)
    html_.add_files(sub_dir_lists, file_lists)


def get_dir_name(root='sdsad'):
    dir_name = root.split(sep='\\')[-1]
    suffix = dir_name.split(sep='_')[-1]

    if suffix.isdigit():
        idx = int(suffix)  # 子文件夹序号
        sub_dir_name = dir_name  # 子文件夹名称
        dir_name = root.split(sep='\\')[-2]
        root = root[:-len(sub_dir_name)]
    else:
        idx = 0
        sub_dir_name = ""

    return dir_name, sub_dir_name, idx, root


class Html(object):
    def __init__(self, name='test', path='D:\\', rewrite=False):
        self.name = name
        self.head = '<html>\n<body>\n'
        self.tail = '</body>\n</html>\n'
        self.context = ''
        self.file_path = path
        self.rewrite = rewrite

    def add_files(self, sub_dir_list, file_list):
        if len(file_list) == 0:
            return

        for i in range(len(sub_dir_list)):
            sub_dir = sub_dir_list[i]
            files = file_list[i]
            for fn in files:
                suffix = fn[-4:]
                if suffix == '.jpg' or suffix == '.png':
                    self.add_img(sub_dir, fn)

        self.write()

    def add_img(self, sub_dir, fn):
        if sub_dir == '':
            self.context += '<img src="' + fn + '"/>\n'
        else:
            self.context += '<img src=".\\' + sub_dir + '\\' + fn + '"/>\n'

    def write(self):
        if len(self.context) == 0:
            try:
                print(self.name, ' is empty')
            except UnicodeEncodeError:
                pass
            return
        else:
            html_name = self.file_path + '\\' + self.name + ".html"
            if not self.rewrite and os.path.exists(html_name):
                return
            try:
                with open(html_name, 'w') as fp:
                    fp.write(self.head)
                    fp.write(self.context)
                    fp.write(self.tail)
            except UnicodeEncodeError:
                print('error', html_name)
            print(self.name, ' write over')


if __name__ == '__main__':
    main(file_path="E:\\")