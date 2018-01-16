# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import pandas as pd
import os


path = "D:\\Cache\\Excel2\\"
path2 = "D:\\Cache\\Excel3\\"
csv_list = os.listdir(path)
f = open("D:\\Cache\\log.csv", "w")
f.write("文件名, 原有数据量, 手机号码重复量\n")
for csv in csv_list:
    fn = path + csv
    df = pd.read_csv(fn, encoding='gbk', dtype={'Area_code': str})
    phone_set = set(df["Number"])
    df['Area_code'] = df['Area_code'].apply(lambda x: x[1:] if x[:2] is '00' else x)
    print("there is {repet} repet row in {file}".format(repet=len(df) - len(phone_set),
                                                        file=csv))
    f.write("{file}, {row1}, {row2}\n".format(file=csv[:-4], row1=len(df), row2=len(df) - len(phone_set)))
    if len(phone_set) == len(df):
        continue
    else:
        df_new = df.drop_duplicates(['Number'])
        print(len(df), len(df_new), len(phone_set))

    df_new.to_csv(path2 + csv, index=False)
