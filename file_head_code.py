# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import os
import re
import codecs


def main():
    filePathSrc = "D:\\Code\\Code\\"  # Path to the folder with files to convert
    for root, dirs, files in os.walk(filePathSrc):
        for fn in files:
            if fn[-3:] == '.py':
                set_file_code(os.path.join(root, fn))


def set_file_code(fn):
    with codecs.open(fn, "r", encoding="utf-8") as f:
        text = f.read()
        f.close()
    pattern = re.compile(r'((?<=coding:)gbk)')
    match = re.search(pattern, string=text)
    if match is None:
        return
    text = text[:match.span()[0]] + 'utf-8' + text[match.span()[1]:]
    with codecs.open(fn, "w", encoding="utf-8") as f:
        f.write(text)
        f.close()


if __name__ == '__main__':
    main()