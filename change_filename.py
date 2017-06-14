# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import os
import shutil


def main(file_path="D:\\Code\\Code\\"):
	flag = 0
	for root, dirs, files in os.walk(file_path):
		for fn in files:
			suffix = fn[-4:]
			if suffix == '.jpg' or suffix == '.png':
				flag += 1
				if root == file_path:
					new_name = get_file_name(flag) + suffix
					os.rename(fn, new_name)
				else:
					new_name = file_path + '\\' + get_file_name(flag) + suffix
					shutil.copyfile(root + '\\' + fn, new_name)


def get_file_name(flag):
	file_name = '000' + str(flag)
	return file_name[-3:]


if __name__ == '__main__':
	main()