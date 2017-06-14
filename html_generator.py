# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import os


def main(file_path="D:\\Code\\Code\\", rewrite=False):
	flag = 0
	for root, dirs, files in os.walk(file_path):
		dir_name = root.split(sep='\\')[-1]
		html_ = Html(dir_name, root, rewrite)
		for fn in files:
			suffix = fn[-4:]
			if suffix == '.jpg' or suffix == '.png':
				flag += 1
				html_.add_img(fn)
		html_.write()
		del html_


class Html():
	def __init__(self, name='test', path='D:\\', rewrite=False):
		self.name = name
		self.head = '<html>\n<body>\n'
		self.tail = '</body>\n</html>\n'
		self.context = ''
		self.file_path = path
		self.rewrite = rewrite

	def add_img(self, fn):
		self.context += '<img src="' + fn + '"/>\n'

	def write(self):
		if len(self.context) == 0:
			print(self.name, ' is empty')
			return
		else:
			html_name = self.file_path + '\\' + self.name + ".html"
			if not self.rewrite and os.path.exists(html_name):
				return
			with open(html_name, 'w') as fp:
				fp.write(self.head)
				fp.write(self.context)
				fp.write(self.tail)
			print(self.name, ' write over')


if __name__ == '__main__':
	main(file_path="D:\\")