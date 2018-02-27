# author='lwz'
# coding:utf-8
import pandas as pd
import numpy as np
import math
import os


class CRAT_tree(object):
    def __init__(self, is_classify=True,
                 min_samples_leaf=0, max_depth=4):  # 构造方法
        self.tree = {}
        self.dataset = pd.DataFrame()  # 数据集
        self.labels = []  # 标签集
        self.traget_col = 'target'
        self.classify = is_classify
        self.min_samples_leaf = min_samples_leaf
        self.max_depth = max_depth
        self.node_id = -1  # 子节点编号
        self.ops = [1, 4]
        self.min_step = 0.001

    def get_node_id(self):
        self.node_id += 1
        return self.node_id

    def load_dataset(self, fname='', target_col='y', labels=''):
        '''
        加载数据
        :param
        fname: 文件名
        target_col: 待分类的列
        :return: None
        '''
        if len(fname) == 0:
            self.dataset = pd.DataFrame(np.eye(4).reshape((4, 4)),
                            columns=['one', 'two', 'three', 'y'])
        else:
            self.dataset = pd.read_csv(fname)

        if target_col not in self.dataset.columns:
            print("we con not find target_col '{}' in columns".format(target_col))
            raise IndexError
        self.target_col = target_col

        if len(labels) == 0:
            self.labels = list(self.dataset.columns)
            self.labels.remove(target_col)
        else:
            self.labels = labels

    def train(self):
        self.tree = self.build_tree(self.dataset, self.labels, deep=0)

    def build_tree(self, dataset=pd.DataFrame(), labels=list(), deep=0):
        # 主函数 构建决策树
        cate_list = dataset[self.target_col]  # 抽取源数据集的决策标签列
        node = Node(self.get_node_id(), message='', head='')
        if self.classify:
            # 程序终止条件1：如果cate_list 只有一种决策标签，停止划分，返回这个决策标签
            tag = dataset.ix[dataset.index[0], self.target_col]
            if len(dataset[self.target_col].value_counts()) < 2:
                # 程序终止条件2：如果数据集的第一个决策标签只有一个，则返回这个决策标签
                node.message = "num:{}\nclass:{}".format(tag, len(dataset))
                return node

            if len(labels) == 1:
                tag = self.max_cate(cate_list)
                node.message = "num:{}\nclass:{}".format(tag, len(dataset))
                return node

        if len(dataset) < self.min_samples_leaf:
            # 若待分类的数据小于叶节点最低值 停止划分
            return node

        if deep > self.max_depth:
            # 若节点深度大于最大深度
            return node

        if len(labels) == 1:
            node.message = "num:{}\nclass:{}".format(len(dataset), tag)
            return node

        # >>>>>>>>>>>>>>>算法核心<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        best_feat, feat_value_list = self.get_best_feat(dataset, labels)
        best_feat_label = labels[best_feat]
        labels.remove(best_feat_label)
        node.message = "num:{}\nlabel:{};".format(len(dataset), best_feat_label)
        # 抽取最优特征值向量
        # unique_vals = set([data[best_feat] for data in dataset])
        for value in feat_value_list:
            sub_labels = labels[:]
            split_data = self.split_dataset(best_feat_label, value, dataset)
            children_node = self.build_tree(split_data, sub_labels, deep+1)  # 递归
            children_node.head = "{}={}\n".format(best_feat_label, value)
            if isinstance(children_node, str):
                print('err')
            else:
                node.add_children_node(children_node)

        return node

    def max_cate(self, dataset):  # 计算出现最多的类别标签：
        tag = dataset.value_counts().index[0]
        return tag

    def get_best_feat(self, dataset, labels): # 计算最优特征
        # 计算特征向量维， 种种最后一列用于类别标签， 因此要减去
        num_values = len(dataset[self.target_col].value_counts())
        if num_values == 1:
            return

        best_var = np.inf
        best_label = ''
        best_value = 0  # 最优划分值

        for label in labels:
            split_values = set(dataset[self.target_col].value_counts())
            for split_value in split_values:
                d_0, d_1 = self.split_dataset(label, split_value, dataset)
                new_var = self.compute_var(d_0, d_1)
                if new_var < best_var:
                    best_var = new_var
                    best_label = label
                    best_value = split_value

        base_var = self.compute_var(dataset)

        if base_var - best_var < self.min_step:
            return

        return [best_var, best_label, best_value]

    def sub_entropy(self, len_1, len_2):
        prob = len_1 / float(len_2)  # 香农熵 = -p * log2(p)
        entropy = prob * math.log(prob, 2)
        return entropy

    def compute_split_info(self, feature_vlist):
        # 计算划分信息 按特征A划分样本集S的广度和均匀度
        num_entries = len(feature_vlist)
        value_count = feature_vlist.value_counts()
        p_list = [float(item) / num_entries for item in value_count]  # p = S_i / sum(S)
        l_list = [item * math.log(item, 2) for item in p_list]  # l = p * log(p, 2)
        split_info = -sum(l_list)  # split_info = -sum(l)
        return split_info, list(value_count.index)

    def compute_var(self, dataset, dataset2=None):  # 计算方差
        var = dataset[self.target_col].var()
        if dataset2 is not None:
            var += dataset2[self.target_col].var()
        return var

    def split_dataset(self, label, value, dataset):  # 划分数据集合 删除特征轴所在列 返回剩余的数值
        try:
            d_1 = dataset[dataset[label] > value]
            d_0 = dataset[dataset[label] <= value]
        except:
            print('err')
        d_1.__delitem__(label)  # 删除特征轴所在列
        d_0.__delitem__(label)  # 删除特征轴所在列
        return d_0, d_1  # 返回剩余的数值

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


def disp_branch(branch, f):
    context = branch.disp()
    f.write(context)
    for sub_branch in branch.sub_nodes:
        disp_branch(sub_branch, f)

def disp_tree(tree):
    with open('Tree0.dot', 'w', encoding='utf-8') as f:
        head = 'digraph Tree {\n node [shape=box] ;\n'
        tail = '}\n'
        f.write(head)
        disp_branch(tree, f)
        f.write(tail)
        print('write over')


class Node(object):
    def __init__(self, flag, message, head):
        '''
        :param flag:  节点编号
        :param message: 节点信息
        '''
        self.flag = flag
        self.message = message
        self.sub_nodes = list()
        self.parent_node = None
        self.head = head

    def add_children_node(self, children_node):
        '''
        设置子节点
        :param children_node:  子节点
        :return:
        '''
        children_node.set_parent_node(self.flag)
        self.sub_nodes.append(children_node)

    def set_parent_node(self, flag):
        '''
        设置父节点
        :param flag:  父节点编号
        :return:
        '''
        self.parent_node = flag

    def disp(self):
        '''
        显示，转换为文本形式
        example:
        1 [label="X[2] <= 0.5\ngini = 0.6559\nsamples = 7382\nvalue = [2371, 1970, 3041]"] ;
        0 -> 1 ;
        :return:
        '''
        context = '{flag} [label="{message}"];\n'.format(flag=self.flag, message=self.head+self.message)
        if self.parent_node is not None:
            context += '{parent_node} -> {child_node};\n'.format(parent_node=self.parent_node, child_node=self.flag)
        return context


def dot2jpg(fn='Tree0.dot'):
    dotPath = "D:\\software\\Graphviz\\bin\\dot.exe"
    sourcePath = os.getcwd() + '\\' + fn
    jpgPath = os.getcwd() + '\\tree.jpg'
    cmd_str = dotPath + ' -Tjpg ' + sourcePath + ' -o ' + jpgPath
    print(cmd_str)
    os.system(cmd_str)


if __name__ == "__main__":
    c45 = C45_tree()
    c45.load_dataset()
    c45.train()
    disp_tree(c45.tree)
    dot2jpg()