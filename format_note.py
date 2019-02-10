# author='lwz'
# coding:utf-8
# 格式化注释缩进
import os

FILE_SUFFIX = []                                    # 文件后缀名列表
NOTE_STR = None                                     # 注释符号
MIN_NOTE_IDX = 12                                   # 注释符号在此之前不移动
STD_NOTE_IDX = 64                                   # 注释符号标准位置
MIN_SPACE_NUM = 2                                   # 代码与注释符号的最小间距MIN_SPACE_NUM
SPACE = "\x20"                                      # 空格符
TAB = SPACE * 4                                     # 制表符


def line_format(line):
    if line[-1] != "\n":
        line += "\n"
    line = line.replace("\t", TAB)
    idx = line.find(NOTE_STR)
    if idx < MIN_NOTE_IDX:
        return line

    for i in range(idx):                            # 若注释内容前全是空格 就默认注释内容为代码 不做处理
        if line[i] != SPACE:
            break
    else:
        return line

    if idx < STD_NOTE_IDX:                          # 增加空格
        tmp = SPACE * (STD_NOTE_IDX - idx)
        new_line = line[:idx] + tmp + line[idx:]
    elif idx > STD_NOTE_IDX:                        # 减少空格
        code_end_idx = idx
        for i in range(idx - 1, STD_NOTE_IDX - 1 - MIN_SPACE_NUM, -1):
            if line[i] != SPACE:
                break
            code_end_idx = i
        new_line = line[:code_end_idx] + SPACE * MIN_SPACE_NUM + line[idx:]
    else:
        new_line = line
    idx_new = new_line.find(NOTE_STR)
    if idx_new != STD_NOTE_IDX:
        print(line, end="")
        print(new_line, end="")
        print(code_end_idx, idx, idx_new)
    return new_line


def file_format(filename):
    EncodeType = "utf-8"
    try:
        with open(filename, "r", encoding=EncodeType) as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        EncodeType = "gbk"
        with open(filename, "r", encoding=EncodeType) as f:
            lines = f.readlines()
    print(filename)
    for i, line in enumerate(lines):
        new_line = line_format(line)
        lines[i] = new_line
    with open(filename, "w", encoding=EncodeType) as f:
        for line in lines:
            f.write(line)


def main(code_path):
    if NOTE_STR is None:
        print("未定义注释符号")
        return
    files = os.listdir(code_path)
    for file in files:
        if len(file.split(".")) == 2 and file.split(".")[1] in FILE_SUFFIX:
            file_format(code_path + file)


if __name__ == "__main__":
    NOTE_STR = "//"
    code_path = "D:\\Code\\"
    FILE_SUFFIX = ["h", "cpp"]
    main(code_path)

