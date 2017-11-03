# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import xlrd  # 打开模块
import xlwt  # 写入模块

style = xlwt.XFStyle()
font = xlwt.Font()
font.name = 'SimSun'  # 指定“宋体”
font.height = 300  # 高度
font.bold = True  # 是否是粗体
style.font = font


def read_excel():
    #    打开文件 读取模式
    workbook1 = xlrd.open_workbook(r'E:\经纪关系维护 2017-11-03.xls')
    workbook2 = xlrd.open_workbook(r'E:\返佣总表 2017-11-03.xls')
    #   打开指定sheet
    new_workbook = xlwt.Workbook('abc')  # 创建excel 得到workbook对象
    sheet1 = workbook1.sheet_by_index(0)
    sheet2 = workbook2.sheet_by_index(0)
    print(sheet1.nrows, sheet2.nrows)
    new_workbook.add_sheet("sheet1")  # 创建 sheet
    new_sheet = new_workbook.get_sheet(0)  # 获取第一个sheet

    id_list = []
    name_list = []
    for i in range(1, sheet1.nrows):
        id_list.append(str(sheet1.cell(i, 5).value))
        name_list.append(sheet1.cell(i, 6).value)

    for j in range(7):  # 写入每一列的名称
        new_sheet.write(0, j, sheet2.cell(0, j).value)

    flag = 0
    id_list2 = []
    for i in range(1, sheet2.nrows):
        id_ = str(sheet2.cell(i, 3).value)
        name = sheet2.cell(i, 4).value
        if id_ not in id_list2:
            id_list2.append(id_)
        else:
            print(id_)

        if id_ in id_list:
            flag += 1
            idx = id_list.index(id_)
            if name != name_list[idx]:
                print('err', id_)

            for j in range(7):  # 写入每一列的名称
                new_sheet.write(flag, j, sheet2.cell(i, j).value)  # 设置单元格字体

            new_sheet.write(flag, 7, i + 1)
            new_sheet.write(flag, 8, idx + 2)

    new_workbook.save(r'E:\经纪关系维护 abc.xls')


if __name__ == '__main__':
    read_excel()
