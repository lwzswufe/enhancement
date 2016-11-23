# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import numpy as np
from sklearn import tree
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_recall_curve
import pandas as pd
import matplotlib.pyplot as plt


"""
criterion: 划分的规则，默认是gini。“gini” = Gini Impurity，取值在0-1之间。“entropy” =
信息增益（information gain）。基尼系数通常是确定平衡的一个指数，用于评价一个国家的收入是否
分配不均衡。这里的基尼不纯度基本上恰好相反：值最小，=0，表明分类之后的元素都归于某一类，越纯
（实际上对应的基尼系数应该是越不平衡）；越趋近于1，表明元素均匀的分散到各个分类里面。
splitter：划分节点的策略，默认是best，算法会根据criterion来选择最好的feature做分割。可以
设置random，算法会随机选择feature做分割；但是实际上，也并非完全的随机，算法也会做一些避免造
成泛化能力丢失的处理。
max_features: 划分的时候需要考虑多少特征，或者全部（默认值）或者一个子集。
max_depth: 最大树深度。避免过拟合的。
min_samples_split: 内部节点上，每一个节点至少需要有的sample个数。避免过拟合的。
min_samples_leaf:  叶子节点上，每一个节点至少需要有的sample个数。避免过拟合的。
min_weight_fraction_leaf: 没研究。
max_leaf_nodes: 最大叶子节点个数。他和max_depth互斥。避免过拟合的。
class_weight:分类的权重。没研究。
random_state : 随机种子，为splitter服务的。如果splitter=random，那么在对同一
组数据做两次预测的时候，会有可能造成决策树不一样（很可能），其原因是使用了不同的
随机种子(random_state)，所以如果一直记录下来随机种子值并一直使用该值的话，就不
会出现多次预测结果不一样的问题。
feature: 特征编号 缺省值为-2
children_self: 该节点的右侧子节点编号 缺省值为-1
threshold： 临界值

结果展开说：

tree_ : Tree 对象（sklearn.tree._tree.Tree)，二叉树。根据这个tree_对象，可以
还原整个决策树的决策过程。关于tree_的细节，可以参考sklearn的官网，如何把tree可视
化，可以参照stackoverflow的问答（参考链接在后面）：
classes_ : 分类的label。
n_classes_ : 分类个数。
feature_importances_ : 特征重要度。越大越重要，表明越是被优先选出来的。
max_features_ : 参与决策树的特征数。
"""


def load_data(fanme='D:\\Cache\\up_limit_00.txt'):
    global data_df, factor_name
    data_df = pd.read_csv(fanme)
    z = list()
    factor_name = list()
    for key in data_df.columns:
        z.append(np.array(data_df[key]))
        factor_name.append(key)
    factor_name.remove('y')
    mat = np.mat(z)
    y = np.array(mat[0, :])[0]
    X = mat[1:, :]
    X = X.T
    if False:
        is_test = np.zeros(len(y))
        is_test[np.random.rand(len(y)) > 0.95] = 1
        test_x = X[is_test > 0, :]
        x = X[is_test < 1, :]
        test_y = y[is_test > 0]
        y = y[is_test < 1]
    else:
        x = X
        y = y
        test_x = x
        test_y = y
    return y, x, test_y, test_x


def regress(y, x, test_x=[]):
    if len(test_x) == 0:
        test_x = x
    clf = DecisionTreeRegressor()
    clf.fit(x, y)
    y_p = clf.predict(test_x)
    plt.scatter(y, y_p)


def classify(y, x, test_y, test_x):
    global data_df, factor_name, left, right, feature, ratio, threshold
    y_c = np.zeros(len(y))
    y_c[y > 0.02] = 1
    y_c[y < -0.02] = -1
    min_n = int(0.05 * len(y))
    clf = DecisionTreeClassifier(max_depth=4, min_samples_leaf=min_n)
    clf.fit(x, y_c)
    y_p = clf.predict(x)
    fname = "D:\\Cache\\tree.txt"
    test_y = y
    with open(fname, 'w') as f:
        tree.export_graphviz(clf, out_file=f)
        f.close()
    factor_exchange(factor_name, fname)
    left = clf.tree_.children_left
    right = clf.tree_.children_right
    feature = clf.tree_.feature
    threshold = clf.tree_.threshold
    disp_tree()
    # precision, recall, thresholds = precision_recall_curve(y_c, clf.predict(x))
    '''''准确率与召回率'''
    print("mean income is:", str(np.average(test_y)),
          "\nwin ratio is: ", str(np.sum(test_y > 0) / len(test_y)))
    print("after training\n"
          "mean class_1 is: ", str(np.average(test_y[y_p > 0])),
          "\nwin ratio is: ", str(np.sum(test_y[y_p > 0] > 0) / np.sum(y_p > 0)),
          "\ntotal class_1 is:", str(np.sum(np.sum(y_p > 0))),
          "\nmean class_0 is: ", str(np.average(test_y[y_p < 0])))


def factor_exchange(factor_name, fname):
    f = open(fname, 'r')
    text = f.read()
    flag = -1
    for factor in factor_name:
        flag += 1
        old_str = 'X[' + str(flag) + ']'
        text = text.replace(old_str, factor)
    f.close()
    f = open(fname, 'w')
    f.write(text)
    f.close()
    '''tree.value 的顺序按照 -1 0 1等的大小排列, 表示训练数据的类别'''


def disp_branch(df, flag):
    global left, right, feature, ratio, threshold
    if left[flag] > 0:
        condition = df.ix[:, feature[flag] + 1] <= threshold[flag]
        ratio[flag] = np.mean(df.y)
        # left
        df_left = df[condition]
        disp_branch(df_left, left[flag])
        # right
        df_right = df[~condition]
        disp_branch(df_right, right[flag])
    else:  # leaf point
        ratio[flag] = np.mean(df.y)


def disp_tree():
    global data_df, ratio
    df = data_df
    ratio = np.zeros(len(left))
    flag = 0
    disp_branch(df, flag)
    print(ratio)


if __name__ == "__main__":
    y, x, test_y, test_x = load_data(fanme='D:\\Cache\\up_limit_01.txt')
    classify(y, x, test_y, test_x)
