# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
from numpy import *
import math
import copy
import pickle


class C45_tree(object):
    def __init__(self):  # 构造方法
        self.tree = {}
        self.dataset = []  # 数据集
        self.labels = []  # 标签集

    def load_dataset(self, labels=['age', 'revenue', 'student', 'credit'],
                     fname='D:\\Cache\\dataset.dat',):
        record_list = []
        f = open(fname, 'r')
        content = f.read()
        row_list = content.splitlines()  # 转化为一维表
        record_list = [row.split("\t") for row in row_list if row.strip()]
        # for row in record_list:
        #    if row[4] == "yes":
        #        row[4] = 1
        #    else:
        #        row[4] = 0
        #    for d in range(len(row)):
        #        row[d] = int(row[d])
        self.dataset = record_list
        self.labels = labels

    def train(self):
        labels = copy.deepcopy(self.labels)
        self.tree = self.build_tree(labels, self.dataset)

    def build_tree(self, label, dataset):
        cate_list = [data[-1] for data in dataset]  # 抽取源数据集的决策标签列
        # 程序终止条件1：如果cate_list 只有一种决策标签，停止划分，返回这个决策标签
        if cate_list.count(cate_list[0]) == len(cate_list):  # count方法 统计出现次数
            return cate_list[0]
        # 程序终止条件2：如果数据集的第一个决策标签只有一个，则返回这个决策标签
        if len(dataset[0]) == 1:
            return self.max_cate(cate_list)
        # 算法核心
        best_feat, feat_value_list = self.get_best_feat(dataset)
        best_feat_label = label[best_feat]
        tree = {best_feat_label:{}}
        del label[best_feat]
        # 抽取最优特征值向量
        # unique_vals = set([data[best_feat] for data in dataset])
        for value in feat_value_list:
            sub_labels = label[:]
            split_data = self.split_dataset(best_feat, value, dataset)
            sub_tree = self.build_tree(sub_labels, split_data)  # 递归
            tree[best_feat_label][value] = sub_tree
        return tree

    def max_cate(self, cate_list):  # 计算出现最多的类别标签：
        items = dict([(cate_list.count(i), i) for i in cate_list])
        return items[max(items.keys())]

    def get_best_feat(self, dataset):
        # 计算特征向量维， 种种最后一列用于类别标签， 因此要减去
        num_features = len(dataset[0]) - 1
        base_entropy = self.compute_entropy(dataset)
        condition_entropy = []  # 初始化条件熵
        split_info = []
        all_feat_vlist = []
        for i in range(num_features):
            feat_list = [example[i] for example in dataset]
            split_i , feature_value_list = self.compute_split_info(feat_list)
            all_feat_vlist.append(feature_value_list)
            split_info.append(split_i)
            result_gain = 0.0
            for value in feature_value_list:
                sub_dataset = self.split_dataset(i, value, dataset)
                appear_num = float(len(sub_dataset))
                sub_entropy = self.compute_entropy(sub_dataset)
                result_gain += (appear_num / len(dataset)) * sub_entropy
            condition_entropy.append(result_gain)
        info_gain_array = base_entropy * ones(num_features) - array(condition_entropy)
        info_gain_ratio = info_gain_array / array(split_info)
        best_feature_index = argsort(-info_gain_ratio)[0]
        return best_feature_index, all_feat_vlist[best_feature_index]

    def sub_entropy(self, len_1, len_2):
        prob = len_1 / float(len_2)  # 香农熵 = -p * log2(p)
        entropy = prob * math.log(prob, 2)
        return entropy

    def compute_split_info(self, feature_vlist):
        num_entries = len(feature_vlist)
        feature_value_setlist = list(set(feature_vlist))
        value_count = [feature_vlist.count(feat_vec) for feat_vec in feature_value_setlist]
        p_list = [float(item) / num_entries for item in value_count]  # p = S_i / sum(S)
        l_list = [item * math.log(item, 2) for item in p_list]  # l = p * log(p, 2)
        split_info = -sum(l_list)  # split_info = -sum(l) 
        return split_info, feature_value_setlist

    def compute_entropy(self, dataset):  # 计算香农熵 entropy=熵
        data_len = float(len(dataset))
        cate_list = [data[-1] for data in dataset]  # 获取类别标签
        # 得到类别为key 出现次数为value的字典
        items = dict([(i, cate_list.count(i)) for i in cate_list])
        info_entropy = 0.0
        for key in items:
            prob = float(items[key]) / data_len  # 香农熵 = -p * log2(p)
            info_entropy -= prob * math.log(prob, 2)
        return info_entropy

    def split_dataset(self, axis, value, dataset):  # 划分数据集合 删除特征轴所在列 返回剩余的数值
        rtn_list = []
        for feat_vec in dataset:
            if feat_vec[axis] == value:
                r_feat_vec = feat_vec[:axis]
                r_feat_vec.extend(feat_vec[axis+1:])
                rtn_list.append(r_feat_vec)
        return rtn_list

    def predict(self, tree, feat_label, test_vec):
        root = tree.keys()[0]
        second_dict = tree[root]
        feat_index = feat_label.index(root)
        key = test_vec[feat_index]
        feat_value = second_dict[key]
        if isinstance(feat_value, dict):
            class_label = self.predict(feat_value, feat_label, test_vec)
        else:
            class_label = feat_value
        return class_label

    def disp_branch(self, branch, level):
        for item in branch.keys():
            print('\n', level, item, end=":")
            if isinstance(branch[item], dict):
                self.disp_branch(branch=branch[item], level=level+'**')
            else:
                print(branch[item], end="")

    def disp_tree(self):
        self.disp_branch(self.tree, '')
        print("")

if __name__ == "__main__":
    c45 = C45_tree()
    c45.load_dataset()
    c45.train()
    c45.disp_tree()
    print(c45.tree)
