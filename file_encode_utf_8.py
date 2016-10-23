# author='lwz'
# coding:gbk
# !/usr/bin/env python3
import os
import sys
filePathSrc = "D:\\Code\\Code\\"  # Path to the folder with files to convert
for root, dirs, files in os.walk(filePathSrc):
    for fn in files:
        if fn[-2:] == '.R':  # Specify type of the files
            notepad.open(root + "\\" + fn)
            notepad.runMenuCommand("Encoding", "Convert to UTF-8")
            notepad.save()
            notepad.close()
