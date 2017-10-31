# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import xlrd  # 打开模块
import xlwt  # 写入模块

style = xlwt.XFStyle()
font = xlwt.Font()
font.name = 'SimSun'    # 指定“宋体”
font.height = 300  # 高度
font.bold = True  # 是否是粗体
style.font = font


def read_excel():
    #    打开文件 读取模式
    workbook = xlrd.open_workbook(r'D:\Cache\附件4 政府性债务投资项目资产明细（3张表）.xlsx')
    #   打开指定sheet
    sheet2 = workbook.sheet_by_name('存量债务')
    
    name_list = list()    # 表名列表
    workbook_dict = {}   # 文件名字典{文件名：workbook对象}
    pre_name = ""        # 前一个表名
    row_flag = 0         # 写入文件行指针
    for i in range(4, sheet2.nrows):
        if pre_name != sheet2.cell(i, 3).value and sheet2.cell(i, 3).value not in name_list:
            # 判断与前一个表名是否一致 表名是否重复
            name_list.append(sheet2.cell(i, 3).value)
            pre_name = sheet2.cell(i, 3).value   # 获取当前表名
            fname = "D:\\Cache\\Test\\" + pre_name + ".xlsx"  # 生成文件名
            print(fname)
            new_workbook = xlwt.Workbook(fname)  # 创建excel 得到workbook对象
            workbook_dict[fname] = new_workbook  # 记录workbook对象
            new_workbook.add_sheet("sheet1")     # 创建 sheet
            new_sheet = new_workbook.get_sheet(0)  # 获取第一个sheet

            new_sheet.write_merge(0, 0, 0, 1, sheet2.cell(1, 0).value)  # 合并单元格
            # write_merge(col_1, col_2, row_1, row_2, title)
            # new_sheet.write(0, 0, sheet2.cell(1, 0).value)  # 写入表格名称  对sheet(0, 0)写入sheet2.cell(1, 0).value

            row_flag = 1                         # 初始化指针 即当前写入行是第一行
            for j in range(19):                 # 写入每一列的名称
                new_sheet.write(row_flag, j, sheet2.cell(3, j).value, style)  # 设置单元格字体

        row_flag += 1                            # 转到下一列
        for j in range(19):
                new_sheet.write(row_flag, j, sheet2.cell(i, j).value)  # 写入每一列的数据

    for fname in workbook_dict:
        workbook_dict[fname].save(fname)         # 保存workbook对象

 
if __name__ == '__main__':
    read_excel()
