import numpy as np
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from matplotlib.colors import ListedColormap
from sklearn.datasets import make_moons
from sklearn.tree import DecisionTreeRegressor


def plot_decision_boundary(clf, X, y, axes=[0, 7.5, 0, 3], iris=True, legend=False, plot_training=True):
    '''
    可视化决策树的划分过程
    :param clf:
    :param X:
    :param y:
    :param axes:
    :param iris:
    :param legend:
    :param plot_training:
    :return:
    '''
    x1s = np.linspace(axes[0], axes[1], 100)
    x2s = np.linspace(axes[2], axes[3], 100)
    x1, x2 = np.meshgrid(x1s, x2s)
    X_new = np.c_[x1.ravel(), x2.ravel()]
    y_pred = clf.predict(X_new).reshape(x1.shape)
    custom_cmap = ListedColormap(['#fafab0','#9898ff','#a0faa0'])
    plt.contourf(x1, x2, y_pred, alpha=0.3, cmap=custom_cmap)
    if not iris:
        custom_cmap2 = ListedColormap(['#7d7d58','#4c4c7f','#507d50'])
        plt.contour(x1, x2, y_pred, cmap=custom_cmap2, alpha=0.8)
    if plot_training:
        plt.plot(X[:, 0][y==0], X[:, 1][y==0], "yo", label="Iris-Setosa")
        plt.plot(X[:, 0][y==1], X[:, 1][y==1], "bs", label="Iris-Versicolor")
        plt.plot(X[:, 0][y==2], X[:, 1][y==2], "g^", label="Iris-Virginica")
        plt.axis(axes)
    if iris:
        plt.xlabel("Petal length", fontsize=14)
        plt.ylabel("Petal width", fontsize=14)
    else:
        plt.xlabel(r"$x_1$", fontsize=18)
        plt.ylabel(r"$x_2$", fontsize=18, rotation=0)
    if legend:
        plt.legend(loc="lower right", fontsize=14)


def Classify():
    '''
    分类决策树的训练与可视化
    :return:
    '''
    iris = load_iris()
    X = iris.data[:, 2:]  # petal length and width
    y = iris.target

    tree_clf = DecisionTreeClassifier(max_depth=2, random_state=42)
    tree_clf.fit(X, y)

    export_graphviz(
        tree_clf,
        out_file=".\\iris_tree.dot",
        feature_names=iris.feature_names[2:],
        class_names=iris.target_names,
        rounded=True,
        filled=True
    )

    plt.figure(figsize=(8, 4))
    plot_decision_boundary(tree_clf, X, y)
    plt.plot([2.45, 2.45], [0, 3], "k-", linewidth=2)
    plt.plot([2.45, 7.5], [1.75, 1.75], "k--", linewidth=2)
    plt.plot([4.95, 4.95], [0, 1.75], "k:", linewidth=2)
    plt.plot([4.85, 4.85], [1.75, 3], "k:", linewidth=2)
    plt.text(1.40, 1.0, "Depth=0", fontsize=15)
    plt.text(3.2, 1.80, "Depth=1", fontsize=13)
    plt.text(4.05, 0.5, "(Depth=2)", fontsize=11)

    plt.show()
    # 预测
    print("预测分属每一个类别的概率：", tree_clf.predict_proba([[5, 1.5]]))
    print("预测类别", tree_clf.predict([[5, 1.5]]))
    # 灵敏度
    # 设置不同的节点深度
    not_widest_versicolor = (X[:, 1] != 1.8) | (y == 2)
    X_tweaked = X[not_widest_versicolor]
    y_tweaked = y[not_widest_versicolor]
    # max_depth=2
    tree_clf_tweaked = DecisionTreeClassifier(max_depth=2, random_state=40)
    tree_clf_tweaked.fit(X_tweaked, y_tweaked)

    plt.figure(figsize=(8, 4))
    plot_decision_boundary(tree_clf_tweaked, X_tweaked, y_tweaked, legend=False)
    plt.plot([0, 7.5], [0.8, 0.8], "k-", linewidth=2)
    plt.plot([0, 7.5], [1.75, 1.75], "k--", linewidth=2)
    plt.text(1.0, 0.9, "Depth=0", fontsize=15)
    plt.text(1.0, 1.80, "Depth=1", fontsize=13)

    plt.show()
    # 设置不同的叶节点数量 防止过拟合
    Xm, ym = make_moons(n_samples=100, noise=0.25, random_state=53)
    # min_samples_leaf=4
    deep_tree_clf1 = DecisionTreeClassifier(random_state=42)
    deep_tree_clf2 = DecisionTreeClassifier(min_samples_leaf=4, random_state=42)
    deep_tree_clf1.fit(Xm, ym)
    deep_tree_clf2.fit(Xm, ym)

    plt.figure(figsize=(11, 4))
    plt.subplot(121)
    plot_decision_boundary(deep_tree_clf1, Xm, ym, axes=[-1.5, 2.5, -1, 1.5], iris=False)
    plt.title("No restrictions", fontsize=16)
    plt.subplot(122)
    plot_decision_boundary(deep_tree_clf2, Xm, ym, axes=[-1.5, 2.5, -1, 1.5], iris=False)
    plt.title("min_samples_leaf = {}".format(deep_tree_clf2.min_samples_leaf), fontsize=14)

    plt.show()

    angle = np.pi / 180 * 20
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    Xr = X.dot(rotation_matrix)

    tree_clf_r = DecisionTreeClassifier(random_state=42)
    tree_clf_r.fit(Xr, y)

    plt.figure(figsize=(8, 3))
    plot_decision_boundary(tree_clf_r, Xr, y, axes=[0.5, 7.5, -1.0, 1], iris=False)

    plt.show()

    Xs = np.random.rand(100, 2) - 0.5
    ys = (Xs[:, 0] > 0).astype(np.float32) * 2
    # 数据对于旋转的敏感性
    angle = np.pi / 4
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    Xsr = Xs.dot(rotation_matrix)

    tree_clf_s = DecisionTreeClassifier(random_state=42)
    tree_clf_s.fit(Xs, ys)
    tree_clf_sr = DecisionTreeClassifier(random_state=42)
    tree_clf_sr.fit(Xsr, ys)

    plt.figure(figsize=(11, 4))
    plt.subplot(121)
    plot_decision_boundary(tree_clf_s, Xs, ys, axes=[-0.7, 0.7, -0.7, 0.7], iris=False)
    plt.subplot(122)
    plot_decision_boundary(tree_clf_sr, Xsr, ys, axes=[-0.7, 0.7, -0.7, 0.7], iris=False)

    plt.show()


def plot_regression_predictions(tree_reg, X, y, axes=[0, 1, -0.2, 1], ylabel="$y$"):
    x1 = np.linspace(axes[0], axes[1], 500).reshape(-1, 1)
    y_pred = tree_reg.predict(x1)
    plt.axis(axes)
    plt.xlabel("$x_1$", fontsize=18)
    if ylabel:
        plt.ylabel(ylabel, fontsize=18, rotation=0)
    plt.plot(X, y, "b.")
    plt.plot(x1, y_pred, "r.-", linewidth=2, label=r"$\hat{y}$")


def Regression():
    '''
    回归树
    :return:
    '''
    np.random.seed(42)
    m = 200
    X = np.random.rand(m, 1)
    y = 4 * (X - 0.5) ** 2
    y = y + np.random.randn(m, 1) / 10

    tree_reg1 = DecisionTreeRegressor(random_state=42, max_depth=2)
    tree_reg2 = DecisionTreeRegressor(random_state=42, max_depth=3)
    tree_reg1.fit(X, y)
    tree_reg2.fit(X, y)

    plt.figure(figsize=(11, 4))
    plt.subplot(121)
    plot_regression_predictions(tree_reg1, X, y)
    for split, style in ((0.1973, "k-"), (0.0917, "k--"), (0.7718, "k--")):
        plt.plot([split, split], [-0.2, 1], style, linewidth=2)
    plt.text(0.21, 0.65, "Depth=0", fontsize=15)
    plt.text(0.01, 0.2, "Depth=1", fontsize=13)
    plt.text(0.65, 0.8, "Depth=1", fontsize=13)
    plt.legend(loc="upper center", fontsize=18)
    plt.title("max_depth=2", fontsize=14)

    plt.subplot(122)
    plot_regression_predictions(tree_reg2, X, y, ylabel=None)
    for split, style in ((0.1973, "k-"), (0.0917, "k--"), (0.7718, "k--")):
        plt.plot([split, split], [-0.2, 1], style, linewidth=2)
    for split in (0.0458, 0.1298, 0.2873, 0.9040):
        plt.plot([split, split], [-0.2, 1], "k:", linewidth=1)
    plt.text(0.3, 0.5, "Depth=2", fontsize=13)
    plt.title("max_depth=3", fontsize=14)

    plt.show()

    export_graphviz(
        tree_reg1,
        out_file=".\\regression_tree.dot",
        feature_names=["x1"],
        rounded=True,
        filled=True
    )
    # 限制叶节点数量 防止过拟合
    tree_reg1 = DecisionTreeRegressor(random_state=42)
    tree_reg2 = DecisionTreeRegressor(random_state=42, min_samples_leaf=10)
    tree_reg1.fit(X, y)
    tree_reg2.fit(X, y)

    x1 = np.linspace(0, 1, 500).reshape(-1, 1)
    y_pred1 = tree_reg1.predict(x1)
    y_pred2 = tree_reg2.predict(x1)

    plt.figure(figsize=(11, 4))

    plt.subplot(121)
    plt.plot(X, y, "b.")
    plt.plot(x1, y_pred1, "r.-", linewidth=2, label=r"$\hat{y}$")
    plt.axis([0, 1, -0.2, 1.1])
    plt.xlabel("$x_1$", fontsize=18)
    plt.ylabel("$y$", fontsize=18, rotation=0)
    plt.legend(loc="upper center", fontsize=18)
    plt.title("No restrictions", fontsize=14)

    plt.subplot(122)
    plt.plot(X, y, "b.")
    plt.plot(x1, y_pred2, "r.-", linewidth=2, label=r"$\hat{y}$")
    plt.axis([0, 1, -0.2, 1.1])
    plt.xlabel("$x_1$", fontsize=18)
    plt.title("min_samples_leaf={}".format(tree_reg2.min_samples_leaf), fontsize=14)

    plt.show()


if __name__ == "__main__":
    # Classify()
    Regression()
