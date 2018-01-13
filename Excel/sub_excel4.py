# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import xlrd  # 打开模块
import xlwt  # 写入模块
import os
import time
import pandas as pd


style = xlwt.XFStyle()
font = xlwt.Font()
font.name = 'SimSun'    # 指定“宋体”
font.height = 300  # 高度
font.bold = True  # 是否是粗体
style.font = font
Province_list1 = ['吉林', '辽宁', '北京', '天津', '上海',
                 '河北', '山西', '山东', '河南', '江苏', '安徽',
                 '浙江', '福建', '广东', '广西', '海南', '江西',
                 '湖北', '湖南', '云南', '贵州', '四川', '西藏',
                 '陕西', '重庆', '宁夏', '甘肃', '新疆', '青海',
                 ]
Province_list2 = ['黑龙江', '内蒙古']
Province_list = Province_list1 + Province_list2
City_list = ['北京', '天津', '上海', '重庆']
path = 'D:\\Cache\\Excel2'


def read_excel():
    #    打开文件 读取模式
    start_time = time.time()
    fn1 = r'C:\Users\lwzswufe\Documents\C 数据.xlsx'
    fn2 = r'C:\Users\lwzswufe\Documents\C.xlsx'
    fn = fn1
    workbook = xlrd.open_workbook(fn)
    sheet_names = workbook.sheet_names()
    df_list = [pd.DataFrame()] * len(Province_list)

    #   打开指定sheet
    for i, sheet in enumerate(workbook.sheets()):
        ncols = sheet.ncols

        if ncols == 5:
            columns = ['Number', 'Type', 'Location', 'Area_code', 'aaa']
        elif ncols == 6:
            columns = ['Name', 'Number', 'Type', 'Location', 'Area_code', 'aaa']
        else:
            print(sheet_names[i], 'cols number error ')
            continue

        print('{} load success used {:.4f}s'.
              format(sheet_names[i], time.time() - start_time))

        try:
            df = pd.read_excel(fn, sheetname=sheet_names[i], names=columns)
        except ValueError:
            print('change columns')
            if ncols == 5:
                columns = ['Name', 'Number', 'Type', 'Location', 'Area_code', 'aaa']
            else:
                columns = ['Number', 'Type', 'Location', 'Area_code', 'aaa']
            df = pd.read_excel(fn, sheetname=sheet_names[i], names=columns)

        print('{} read success used {:.4f}s'.
              format(sheet_names[i], time.time() - start_time))

        if ncols == 5:
            df['Name'] = ''

        df['province_id'] = df.Location.apply(get_province_id)
        df['Area_code'] = df['Area_code'].apply(get_area_code)

        for i in range(len(Province_list)):
            if len(df_list[i]) == 0:
                df_list[i] = df[df['province_id'] == i]
            else:
                df_list[i] = pd.concat([df_list[i], df[df['province_id'] == i]], ignore_index=True)

    for i in range(len(Province_list)):
        df_list[i].to_csv(path+'\\'+Province_list[i] + '.csv', index=False)


def get_province_id(province_name):
    if not isinstance(province_name, str):
        return -1

    if len(province_name) <= 2:
        if province_name in City_list:
            return Province_list.index(province_name)
        else:
            # print(province_name)
            return -1
    else:
        if province_name[:2] in Province_list:
            return Province_list.index(province_name[:2])
        elif province_name[:3] in Province_list2:
            return Province_list2.index(province_name[:3])
        else:
            # print(province_name)
            return -1


def get_area_code(c):
    return'0' + str(c)


if __name__ == '__main__':
    read_excel()