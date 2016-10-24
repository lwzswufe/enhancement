# author='lwz'
# coding:gbk
# !/usr/bin/env python3
import os


def main():
    filePathSrc = "D:\\Code\\Code\\"  # Path to the folder with files to convert
    file_num = [0, 0, 0]
    row_nom = [0, 0, 0]
    for root, dirs, files in os.walk(filePathSrc):
        for fn in files:
            if fn[-3:] == '.py':
                file_num[0] += 1
                row_nom[0] += stat(os.path.join(root, fn))
            elif fn[-2:] == '.m':  # Specify type of the files
                file_num[1] += 1
                row_nom[1] += stat(os.path.join(root, fn))
            elif fn[-2:] == '.R':
                file_num[2] += 1
                row_nom[2] += stat(os.path.join(root, fn))
    for i in range(len(file_num)):
        print(str(file_num[i]) + '  files' + str(row_nom[i]) + 'rows')


def stat(fn):
    f = open(fn, 'rb')
    try:
        lines = f.readlines()
    except Exception as err:
        print(err)
        print(fn)
        lines = list()
    flag = len(lines)
    return flag


if __name__ == '__main__':
    main()

