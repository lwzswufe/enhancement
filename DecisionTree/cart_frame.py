# author='lwz'
# coding:utf-8
import numpy as np
import pandas as pd
import math
import os


'''

  str类型 与 bool类型 的变量是分类变量
非str类型 与 bool类型 的变量默认是有序变量
'''


class CartTree(object):
    def __init__(self, target_col="", labels=[],
                 min_samples_leaf=0, max_depth=4):  # 构造方法
        self.tree = {}
        self.dataset = pd.DataFrame()  # 数据集
        self.labels = labels  # 标签集
        self.traget_col = target_col
        self.time_phase = 0
        self.classify = False
        self.min_samples_leaf = min_samples_leaf
        self.max_depth = max_depth
        self.node_id = -1  # 子节点编号
        self.min_step = 0.001
        self.ordinal_sample_num = 10  # 连续变量采样数

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
            self.dataset = pd.DataFrame(np.eye(4).reshape((4, 4)), columns=['one', 'two', 'three', 'y'])
        else:
            self.dataset = pd.read_csv(fname)

        if target_col not in self.dataset.columns:
            print("we con not find target_col '{}' in columns".format(target_col))
            raise IndexError

        self.target_col = target_col
        self.is_classify(self.dataset[target_col][0])
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
            tag = dataset.loc[dataset.index[0], self.target_col]
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
        # best_feat, feat_value_list = self.get_best_feat(dataset, labels)
        return_data = self.get_best_feat(dataset, labels)
        if return_data is None:
            return node
        else:
            best_var, best_label, best_value = return_data

        node.message = "num:{}\nlabel:{};".format(len(dataset), best_label)
        # 划分数据
        if best_value is None:
            data_list, tag_list = self.split_dataset_categorical(best_label, dataset)
        else:
            data_list, tag_list = self.split_dataset_ordinal(best_label, best_value, dataset)
        # 创建子节点
        for i, sub_data in enumerate(data_list):
            children_node = self.build_tree(sub_data, best_label, deep + 1)  # 递归
            children_node.head = tag_list[i]
            if isinstance(children_node, str):
                print('err')
            else:
                node.add_children_node(children_node)
        return node

    @staticmethod
    def max_cate(dataset):
        '''
        # 计算出现最多的类别标签
        :param dataset: 数据集
        :return:
        '''
        tag = dataset.value_counts().index[0]
        return tag

    def get_best_feat(self, dataset, labels):
        '''
        计算最优特征
        #计算特征向量维， 种类最后一列用于类别标签， 因此要减去
        :param dataset:
        :param labels:
        :return:
        '''

        num_values = len(dataset[self.target_col].value_counts())
        # 只剩一种类型 到达叶节点
        if num_values == 1:
            return

        best_var = np.inf
        best_label = ''
        best_value = 0  # 最优划分值
        # 遍历标签
        for label in labels:
            if isinstance(dataset[label].dtype, pd.CategoricalDtype) or \
               isinstance(dataset[label][0], bool):
                data_list = self.split_dataset_categorical(dataset, label)
                new_var = self.compute_var(data_list)
                best_value = None
            else:
                new_value, new_var = self.get_best_ordinal_split_value(dataset, label)
            if new_var < best_var:
                best_var = new_var
                best_value = new_value

        base_var = self.compute_var(dataset)
        # 本次信息增益小于最低要求
        if base_var - best_var < self.min_step:
            return None

        data_list = self.split_dataset(best_label, best_value, dataset)
        min_data_length = [len(data) for data in data_list]
        # 本节点无法再细分
        if min_data_length < self.min_samples_leaf:
            return None
        # 正常返回
        return best_var, best_label, best_value

    @staticmethod
    def sub_entropy(len_1, len_2):
        '''
        计算香农熵 = -p * log2(p)
        :param len_1: 样本1数量
        :param len_2: 样本2数量
        :return:
        '''
        prob = len_1 / float(len_2)
        entropy = prob * math.log(prob, 2)
        return entropy

    @staticmethod
    def compute_split_info(feature_vlist):
        '''
        计算划分信息 按特征A划分样本集S的广度和均匀度
        :param feature_vlist:
        :return:
        '''
        num_entries = len(feature_vlist)
        value_count = feature_vlist.value_counts()
        p_list = [float(item) / num_entries for item in value_count]  # p = S_i / sum(S)
        l_list = [item * math.log(item, 2) for item in p_list]  # l = p * log(p, 2)
        split_info = -sum(l_list)  # split_info = -sum(l)
        return split_info, list(value_count.index)

    def compute_var(self, datalist=[]):
        '''
        计算方差
        '''
        var = 0
        for data in datalist:
            var += data[self.target_col].var()
        return var

    def get_best_ordinal_split_value(self, dataset, label):
        '''
        :param label:
        :param value:
        :param dataset:
        :return:
        '''
        best_var = np.inf
        best_value = 0  # 最优划分值
        arg_min = dataset[label].sort()
        max_idx = len(dataset[label]) - 1
        split_values = set([round(i * 1.0 / (self.ordinal_sample_num + 1) * max_idx) for i in range(self.ordinal_sample_num)])
        for split_value in split_values:
            data_list = self.split_dataset_ordinal(label, split_value, dataset)
            new_var = self.compute_var(data_list)
            if new_var < best_var:
                best_var = new_var
                best_value = split_value
        return best_value, best_var

    @staticmethod
    def split_dataset_categorical(label, dataset):
        '''
        分类变量划分数据集合 删除特征轴所在列 返回剩余的数值
        '''
        df_list = []
        tag_list = []
        for label_, df in dataset.groupby(label):
            df.__delitem__(label)  # 删除特征轴所在列
            df_list.append(df)
            tag_list.append("{}={}".format(label, label_))
        return df_list, tag_list  # 返回剩余的数值

    @staticmethod
    def split_dataset_ordinal(label, value, dataset):
        '''
        有序变量划分数据集合 不删除特征轴所在列
        '''
        try:
            d_0 = dataset[dataset[label] <= value]
            d_1 = dataset[dataset[label] > value]
            tag_0 = "{}<={}".format(label, value)
            tag_1 = "{}>{}".format(label, value)
        except Exception as err:
            print(err)
            return [], []
        return [d_0, d_1], [tag_0, tag_1]  # 返回剩余的数值

    @staticmethod
    def is_classify(x):
        '''
        判断变量x是不是分类变量
        '''
        if isinstance(x, str) or isinstance(x, bool):
            return True
        else:
            return False

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
    dotPath = "C:\\Program Files (x86)\\Graphviz2.38\\bin\\dot.exe"
    sourcePath = os.getcwd() + '\\' + fn
    jpgPath = os.getcwd() + '\\tree.jpg'
    cmd_str = dotPath + ' -Tjpg ' + sourcePath + ' -o ' + jpgPath
    print(cmd_str)
    os.system(cmd_str)


if __name__ == "__main__":
    crat = CartTree()
    crat.load_dataset("data.csv", "class")
    crat.train()
    disp_tree(crat.tree)
    dot2jpg()