# Common imports
import numpy as np
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_openml, load_files
from scipy.io import loadmat
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.base import clone
from sklearn.base import BaseEstimator
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_curve
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsOneClassifier
# to make this notebook's output stable across runs
np.random.seed(42)

mpl.rc('axes', labelsize=14)
mpl.rc('xtick', labelsize=12)
mpl.rc('ytick', labelsize=12)


def sort_by_target(mnist):
    reorder_train = np.array(sorted([(target, i) for i, target in enumerate(mnist.target[:60000])]))[:, 1]
    reorder_test = np.array(sorted([(target, i) for i, target in enumerate(mnist.target[60000:])]))[:, 1]
    mnist.data[:60000] = mnist.data[reorder_train]
    mnist.target[:60000] = mnist.target[reorder_train]
    mnist.data[60000:] = mnist.data[reorder_test + 60000]
    mnist.target[60000:] = mnist.target[reorder_test + 60000]


def plot_digit(data, label=None):
    '''
    绘制图片
    :param data: 样本
    :param label: 标签
    :return:
    '''
    image = data.reshape(28, 28)
    plt.imshow(image, cmap=mpl.cm.binary,
               interpolation="nearest")
    if label is not None:
        plt.title("label={:.0f}".format(label))
    plt.axis("off")


def plot_digits(instances, images_per_row=10, **options):
    '''
    绘制多个图片
    :param instances:
    :param images_per_row:
    :param options:
    :return:
    '''
    size = 28
    images_per_row = min(len(instances), images_per_row)
    images = [instance.reshape(size,size) for instance in instances]
    n_rows = (len(instances) - 1) // images_per_row + 1
    row_images = []
    n_empty = n_rows * images_per_row - len(instances)
    images.append(np.zeros((size, size * n_empty)))
    for row in range(n_rows):
        rimages = images[row * images_per_row : (row + 1) * images_per_row]
        row_images.append(np.concatenate(rimages, axis=1))
    image = np.concatenate(row_images, axis=0)
    plt.imshow(image, cmap = mpl.cm.binary, **options)
    plt.axis("off")


def load_data():
    # mnist = fetch_openml('mnist_784', version=1, cache=True)
    # mnist = load_files("D:\\data\\mnist")
    # 读取本地数据
    mnist = loadmat("D:\\data\\mnist\\mldata\\mnist-original.mat")
    # mnist = load_files('D:\\data\\mnist\\mnist-original.mat')
    # fetch_openml() returns targets as strings
    # mnist.target = mnist.target.astype(np.int8)
    # fetch_openml() returns an unsorted dataset
    # sort_by_target(mnist)
    mnist["data"] = mnist["data"].T
    mnist["label"] = mnist["label"].flatten()
    X, y = mnist["data"], mnist["label"]
    return X, y


def main():
    X, y = load_data()

    print("X.shape:", X.shape)
    print("y.shape:", y.shape)
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>显示图片<<<<<<<<<<<<<<<<<<<<<<<
    plot_digit(X[36000], y[36000])

    plt.figure(figsize=(9, 9))
    example_images = np.r_[X[:12000:600], X[13000:30600:600], X[30600:60000:590]]
    plot_digits(example_images, images_per_row=10)
    plt.show()
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>划分训练集 测试集<<<<<<<<<<<<<<<<<<<<<<<
    X_train, X_test, y_train, y_test = X[:60000], X[60000:], y[:60000], y[60000:]
    shuffle_index = np.random.permutation(60000)
    X_train, y_train = X_train[shuffle_index], y_train[shuffle_index]


class Never5Classifier(BaseEstimator):
    def fit(self, X, y=None):
        pass
    def predict(self, X):
        return np.zeros((len(X), 1), dtype=bool)


def plot_precision_recall_vs_threshold(precisions, recalls, thresholds):
    '''
    绘制 精度 召回率 阈值曲线
    :param precisions:
    :param recalls:
    :param thresholds:
    :return:
    '''
    plt.figure(figsize=(8, 4))
    plt.plot(thresholds, precisions[:-1], "b--", label="Precision", linewidth=2)
    plt.plot(thresholds, recalls[:-1], "g-", label="Recall", linewidth=2)
    plt.xlabel("Threshold", fontsize=16)
    plt.legend(loc="upper left", fontsize=16)
    plt.ylim([0, 1])


def plot_precision_vs_recall(precisions, recalls):
    '''
    绘制精度召回率函数图
    :param precisions:
    :param recalls:
    :return:
    '''
    plt.plot(recalls, precisions, "b-", linewidth=2)
    plt.xlabel("Recall", fontsize=16)
    plt.ylabel("Precision", fontsize=16)
    plt.axis([0, 1, 0, 1])


def plot_roc_curve(fpr, tpr, label=None):
    '''
    绘制ROC曲线
    :param fpr:
    :param tpr:
    :param label:
    :return:
    '''
    plt.plot(fpr, tpr, linewidth=2, label=label)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.axis([0, 1, 0, 1])
    plt.xlabel('False Positive Rate', fontsize=16)
    plt.ylabel('True Positive Rate', fontsize=16)


def binary_train():
    X, y = load_data()
    X_train, X_test, y_train, y_test = X[:60000], X[60000:], y[:60000], y[60000:]
    shuffle_index = np.random.permutation(60000)
    X_train, y_train = X_train[shuffle_index], y_train[shuffle_index]
    y_train_5 = (y_train == 5)
    y_test_5 = (y_test == 5)
    # >>>>>>>>>>>>>>>>>>>>>>>>>随机梯度下降法训练的线性分类器<<<<<<<<<<<<<<<<<<<<<<<<
    sgd_clf = SGDClassifier(max_iter=5, tol=-np.infty, random_state=42)
    sgd_clf.fit(X_train, y_train_5)

    # for i in range(10):
    y_pre = sgd_clf.predict(X_test[0:10000:1000])
    for i in range(10):
        print("Xtest[{}] is {:.0f} predict is_5:{}".format(i*1000, y_test[i*1000], y_pre[i]))

    # 使用交叉验证
    cross_val_score(sgd_clf, X_train, y_train_5, cv=3, scoring="accuracy")
    # 使用K-fold交叉验证  折叠3次
    skfolds = StratifiedKFold(n_splits=3, random_state=42)
    # 折叠交叉验证
    for train_index, test_index in skfolds.split(X_train, y_train_5):
        clone_clf = clone(sgd_clf)
        X_train_folds = X_train[train_index]
        y_train_folds = (y_train_5[train_index])
        X_test_fold = X_train[test_index]
        y_test_fold = (y_train_5[test_index])

        clone_clf.fit(X_train_folds, y_train_folds)
        y_pred = clone_clf.predict(X_test_fold)
        n_correct = sum(y_pred == y_test_fold)
        print("准确率", n_correct / len(y_pred))

    never_5_clf = Never5Classifier()
    cross_score = cross_val_score(never_5_clf, X_train, y_train_5, cv=3, scoring="accuracy")
    print(cross_score)
    # >>>>>>>>>>>>>>>>>>>>>>混淆矩阵<<<<<<<<<<<<<<<<<<<
    y_train_pred = cross_val_predict(sgd_clf, X_train, y_train_5, cv=3)
    cfs_mat = confusion_matrix(y_train_5, y_train_pred)
    print("混淆矩阵:", cfs_mat)
    # >>>>>>>>>>>>>>>>>>>>>>精度<<<<<<<<<<<<<<<<<<<<<<<
    prec = precision_score(y_train_5, y_train_pred)
    print("精度:{:.3f}  真正 / (假正 + 真正) ".format(prec))
    # >>>>>>>>>>>>>>>>>>>>>>召回率<<<<<<<<<<<<<<<<<<<
    recl = recall_score(y_train_5, y_train_pred)
    print("召回率:{:.3f}  真负 / (假负 + 真负) ".format(recl))
    # >>>>>>>>>>>>>>>>>>>>>>F1分数<<<<<<<<<<<<<<<<<<<
    F1 = f1_score(y_train_5, y_train_pred)
    print("F1分数:{:.3f}  精度 召回率 的调和平均数".format(F1))
    # >>>>>>>>>>>>>>>>>>>>>>使用阈值调节 精度 召回率 <<<<<<<<<<<<<<<<<<<
    # 获取每个样本的得分
    y_scores = sgd_clf.decision_function(X_test)
    threshold = 0
    y_pred = (y_scores > threshold)
    prec = precision_score(y_test_5, y_pred)
    recl = recall_score(y_test_5, y_pred)
    print("精度:{:.3f} 召回率:{:.3f}".format(prec, recl))
    # 提高阈值 提高精度 降低召回率
    threshold = 200000
    y_pred = (y_scores > threshold)
    prec = precision_score(y_test_5, y_pred)
    recl = recall_score(y_test_5, y_pred)
    print("精度:{:.3f} 召回率:{:.3f}".format(prec, recl))
    # 获取所有样本得分
    y_scores = cross_val_predict(sgd_clf, X_train, y_train_5, cv=3,
                                 method="decision_function")
    if y_scores.ndim == 2:
        y_scores = y_scores[:, 1]
    # 绘制 精度 召回率 阈值曲线
    precisions, recalls, thresholds = precision_recall_curve(y_train_5, y_scores)
    plot_precision_recall_vs_threshold(precisions, recalls, thresholds)
    plt.xlim([-700000, 700000])
    plt.show()
    # 绘制 精度 召回率 函数曲线
    plt.figure(figsize=(8, 6))
    plot_precision_vs_recall(precisions, recalls)
    plt.show()
    # 绘制ROC曲线
    fpr, tpr, thresholds = roc_curve(y_train_5, y_scores)
    plt.figure(figsize=(8, 6))
    plot_roc_curve(fpr, tpr)
    plt.show()
    # 随机森林分类
    forest_clf = RandomForestClassifier(n_estimators=10, random_state=42)
    y_probas_forest = cross_val_predict(forest_clf, X_train, y_train_5, cv=3,
                                        method="predict_proba")
    y_scores_forest = y_probas_forest[:, 1]  # score = proba of positive class
    fpr_forest, tpr_forest, thresholds_forest = roc_curve(y_train_5, y_scores_forest)
    # ROC曲线对比
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, "b:", linewidth=2, label="SGD")
    plot_roc_curve(fpr_forest, tpr_forest, "Random Forest")
    plt.legend(loc="lower right", fontsize=16)
    plt.show()


def multi_train():
    X, y = load_data()
    X_train, X_test, y_train, y_test = X[:60000], X[60000:], y[:60000], y[60000:]
    shuffle_index = np.random.permutation(60000)
    X_train, y_train = X_train[shuffle_index], y_train[shuffle_index]
    # 使用OneVsOneClassifier将二元分类器改为多元分类器
    ovo_clf = OneVsOneClassifier(SGDClassifier(max_iter=5, tol=-np.infty, random_state=42))
    ovo_clf.fit(X_train, y_train)
    y_train_pred = ovo_clf.predict(X_train)
    conf_mx = confusion_matrix(y_train, y_train_pred)
    print(conf_mx)


if __name__ == "__main__":
    # main()
    # binary_train()
    multi_train()