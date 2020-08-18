
# Common imports
import numpy as np
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn import datasets
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.datasets import make_moons
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVC
from sklearn.svm import LinearSVR
from sklearn.svm import SVR
from sklearn.base import BaseEstimator
np.random.seed(42)


def plot_svc_decision_boundary(svm_clf, xmin, xmax):
    '''
    绘制SVM决策分类线
    :param svm_clf:
    :param xmin:
    :param xmax:
    :return:
    '''
    w = svm_clf.coef_[0]
    b = svm_clf.intercept_[0]

    # At the decision boundary, w0*x0 + w1*x1 + b = 0
    # => x1 = -w0/w1 * x0 - b/w1
    x0 = np.linspace(xmin, xmax, 200)
    decision_boundary = -w[0]/w[1] * x0 - b/w[1]

    margin = 1/w[1]
    gutter_up = decision_boundary + margin
    gutter_down = decision_boundary - margin

    svs = svm_clf.support_vectors_
    plt.scatter(svs[:, 0], svs[:, 1], s=180, facecolors='#FFAAAA')
    plt.plot(x0, decision_boundary, "k-", linewidth=2)
    plt.plot(x0, gutter_up, "k--", linewidth=2)
    plt.plot(x0, gutter_down, "k--", linewidth=2)


def LinearClassify():
    '''
    线性SVM分类
    :return:
    '''
    iris = datasets.load_iris()
    X = iris["data"][:, (2, 3)]  # petal length, petal width
    y = iris["target"]
    # 提取两类鸢尾花
    setosa_or_versicolor = (y == 0) | (y == 1)
    X = X[setosa_or_versicolor]
    y = y[setosa_or_versicolor]
    # SVM Classifier model
    svm_clf = SVC(kernel="linear", C=float("inf"))
    svm_clf.fit(X, y)
    # 为测试线提供x值
    x0 = np.linspace(0, 5.5, 200)
    # 测试分类线1
    pred_1 = 5 * x0 - 20
    # 测试分类线2
    pred_2 = x0 - 1.8
    # 测试分类线3
    pred_3 = 0.1 * x0 + 0.5

    plt.figure(figsize=(12, 2.7))
    # 测试分类效果图
    plt.subplot(121)
    plt.plot(x0, pred_1, "g--", linewidth=2)
    plt.plot(x0, pred_2, "m-", linewidth=2)
    plt.plot(x0, pred_3, "r-", linewidth=2)
    plt.plot(X[:, 0][y == 1], X[:, 1][y == 1], "bs", label="Iris-Versicolor")
    plt.plot(X[:, 0][y == 0], X[:, 1][y == 0], "yo", label="Iris-Setosa")
    plt.xlabel("Petal length", fontsize=14)
    plt.ylabel("Petal width", fontsize=14)
    plt.legend(loc="upper left", fontsize=14)
    plt.axis([0, 5.5, 0, 2])
    # SVM分类效果图
    plt.subplot(122)
    plot_svc_decision_boundary(svm_clf, 0, 5.5)
    plt.plot(X[:, 0][y == 1], X[:, 1][y == 1], "bs")
    plt.plot(X[:, 0][y == 0], X[:, 1][y == 0], "yo")
    plt.xlabel("Petal length", fontsize=14)
    plt.axis([0, 5.5, 0, 2])
    plt.show()
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> SVM对特征缩放的敏感度  <<<<<<<<<<<<<<<<<<<<<<<<<<<<
    Xs = np.array([[1, 50], [5, 20], [3, 80], [5, 60]]).astype(np.float64)
    ys = np.array([0, 0, 1, 1])
    svm_clf = SVC(kernel="linear", C=100)
    svm_clf.fit(Xs, ys)
    # 对原始数据的SVM分类结果绘图
    plt.figure(figsize=(12, 3.2))
    plt.subplot(121)
    plt.plot(Xs[:, 0][ys == 1], Xs[:, 1][ys == 1], "bo")
    plt.plot(Xs[:, 0][ys == 0], Xs[:, 1][ys == 0], "ms")
    plot_svc_decision_boundary(svm_clf, 0, 6)
    plt.xlabel("$x_0$", fontsize=20)
    plt.ylabel("$x_1$  ", fontsize=20, rotation=0)
    plt.title("Unscaled", fontsize=16)
    plt.axis([0, 6, 0, 90])
    # 对原始数据进行归一化处理
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(Xs)
    svm_clf.fit(X_scaled, ys)
    # 对归一化后数据绘图
    plt.subplot(122)
    plt.plot(X_scaled[:, 0][ys == 1], X_scaled[:, 1][ys == 1], "bo")
    plt.plot(X_scaled[:, 0][ys == 0], X_scaled[:, 1][ys == 0], "ms")
    plot_svc_decision_boundary(svm_clf, -2, 2)
    plt.xlabel("$x_0$", fontsize=20)
    plt.title("Scaled", fontsize=16)
    plt.axis([-2, 2, -2, 2])
    plt.show()
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> SVM硬间隔分类对异常点敏感  <<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # 设置异常点
    X_outliers = np.array([[3.4, 1.3], [3.2, 0.8]])
    y_outliers = np.array([0, 0])
    # 添加线性可分异常点到原有数据集
    Xo1 = np.concatenate([X, X_outliers[:1]], axis=0)
    yo1 = np.concatenate([y, y_outliers[:1]], axis=0)
    # 添加线性不可分异常点到原有数据集
    Xo2 = np.concatenate([X, X_outliers[1:]], axis=0)
    yo2 = np.concatenate([y, y_outliers[1:]], axis=0)
    # SVM线性分类
    svm_clf2 = SVC(kernel="linear", C=10 ** 9)
    svm_clf2.fit(Xo2, yo2)

    plt.figure(figsize=(12, 2.7))
    # 带有线性可分异常点的数据集分类效果
    plt.subplot(121)
    plt.plot(Xo1[:, 0][yo1 == 1], Xo1[:, 1][yo1 == 1], "bs")
    plt.plot(Xo1[:, 0][yo1 == 0], Xo1[:, 1][yo1 == 0], "yo")
    plt.text(0.3, 1.0, "Impossible!", fontsize=24, color="red")
    plt.xlabel("Petal length", fontsize=14)
    plt.ylabel("Petal width", fontsize=14)
    plt.annotate("Outlier",
                 xy=(X_outliers[0][0], X_outliers[0][1]),
                 xytext=(2.5, 1.7),
                 ha="center",
                 arrowprops=dict(facecolor='black', shrink=0.1),
                 fontsize=16,
                 )
    plt.axis([0, 5.5, 0, 2])
    # 带有线性不可分异常点的数据集分类效果
    plt.subplot(122)
    plt.plot(Xo2[:, 0][yo2 == 1], Xo2[:, 1][yo2 == 1], "bs")
    plt.plot(Xo2[:, 0][yo2 == 0], Xo2[:, 1][yo2 == 0], "yo")
    plot_svc_decision_boundary(svm_clf2, 0, 5.5)
    plt.xlabel("Petal length", fontsize=14)
    plt.annotate("Outlier",
                 xy=(X_outliers[1][0], X_outliers[1][1]),
                 xytext=(3.2, 0.08),
                 ha="center",
                 arrowprops=dict(facecolor='black', shrink=0.1),
                 fontsize=16,
                 )
    plt.axis([0, 5.5, 0, 2])

    plt.show()


def SoftLineClassify():
    '''
    软间隔线性SVM分类
    :return:
    '''
    iris = datasets.load_iris()
    X = iris["data"][:, (2, 3)]  # petal length, petal width
    y = (iris["target"] == 2).astype(np.float64)  # Iris-Virginica

    scaler = StandardScaler()
    # C=1 分类间隔窄
    svm_clf1 = LinearSVC(C=1, loss="hinge", random_state=42)
    # C=100 分类间隔宽
    svm_clf2 = LinearSVC(C=100, loss="hinge", random_state=42)

    scaled_svm_clf1 = Pipeline([
        ("scaler", scaler),
        ("linear_svc", svm_clf1),
    ])
    scaled_svm_clf2 = Pipeline([
        ("scaler", scaler),
        ("linear_svc", svm_clf2),
    ])

    scaled_svm_clf1.fit(X, y)
    scaled_svm_clf2.fit(X, y)

    # Convert to unscaled parameters
    # 提取分类参数
    b1 = svm_clf1.decision_function([-scaler.mean_ / scaler.scale_])
    b2 = svm_clf2.decision_function([-scaler.mean_ / scaler.scale_])
    w1 = svm_clf1.coef_[0] / scaler.scale_
    w2 = svm_clf2.coef_[0] / scaler.scale_
    svm_clf1.intercept_ = np.array([b1])
    svm_clf2.intercept_ = np.array([b2])
    svm_clf1.coef_ = np.array([w1])
    svm_clf2.coef_ = np.array([w2])

    # Find support vectors (LinearSVC does not do this automatically)
    # 绘制分类线
    t = y * 2 - 1
    support_vectors_idx1 = (t * (X.dot(w1) + b1) < 1).ravel()
    support_vectors_idx2 = (t * (X.dot(w2) + b2) < 1).ravel()
    svm_clf1.support_vectors_ = X[support_vectors_idx1]
    svm_clf2.support_vectors_ = X[support_vectors_idx2]

    plt.figure(figsize=(12, 3.2))
    # 窄间隔分类线
    plt.subplot(121)
    plt.plot(X[:, 0][y == 1], X[:, 1][y == 1], "g^", label="Iris-Virginica")
    plt.plot(X[:, 0][y == 0], X[:, 1][y == 0], "bs", label="Iris-Versicolor")
    plot_svc_decision_boundary(svm_clf1, 4, 6)
    plt.xlabel("Petal length", fontsize=14)
    plt.ylabel("Petal width", fontsize=14)
    plt.legend(loc="upper left", fontsize=14)
    plt.title("$C = {}$".format(svm_clf1.C), fontsize=16)
    plt.axis([4, 6, 0.8, 2.8])
    # 宽间隔分类线
    plt.subplot(122)
    plt.plot(X[:, 0][y == 1], X[:, 1][y == 1], "g^")
    plt.plot(X[:, 0][y == 0], X[:, 1][y == 0], "bs")
    plot_svc_decision_boundary(svm_clf2, 4, 6)
    plt.xlabel("Petal length", fontsize=14)
    plt.title("$C = {}$".format(svm_clf2.C), fontsize=16)
    plt.axis([4, 6, 0.8, 2.8])

    plt.show()


def plot_dataset(X, y, axes):
    '''
    绘制数据集
    :param X:
    :param y:
    :param axes:
    :return:
    '''
    plt.plot(X[:, 0][y==0], X[:, 1][y==0], "bs")
    plt.plot(X[:, 0][y==1], X[:, 1][y==1], "g^")
    plt.axis(axes)
    plt.grid(True, which='both')
    plt.xlabel(r"$x_1$", fontsize=20)
    plt.ylabel(r"$x_2$", fontsize=20, rotation=0)


def plot_predictions(clf, axes):
    '''
    绘制预测分类区域图
    :param clf:
    :param axes:
    :return:
    '''
    x0s = np.linspace(axes[0], axes[1], 100)
    x1s = np.linspace(axes[2], axes[3], 100)
    x0, x1 = np.meshgrid(x0s, x1s)
    X = np.c_[x0.ravel(), x1.ravel()]
    y_pred = clf.predict(X).reshape(x0.shape)
    y_decision = clf.decision_function(X).reshape(x0.shape)
    plt.contourf(x0, x1, y_pred, cmap=plt.cm.brg, alpha=0.2)
    plt.contourf(x0, x1, y_decision, cmap=plt.cm.brg, alpha=0.1)


def PolyomialClassify():
    '''
    多项式SVM
    :return:
    '''
    X1D = np.linspace(-4, 4, 9).reshape(-1, 1)
    X2D = np.c_[X1D, X1D ** 2]
    y = np.array([0, 0, 1, 1, 1, 1, 1, 0, 0])

    plt.figure(figsize=(11, 6))
    # 线性不可分
    plt.subplot(121)
    plt.grid(True, which='both')
    plt.axhline(y=0, color='k')
    plt.plot(X1D[:, 0][y == 0], np.zeros(4), "bs")
    plt.plot(X1D[:, 0][y == 1], np.zeros(5), "g^")
    plt.gca().get_yaxis().set_ticks([])
    plt.xlabel(r"$x_1$", fontsize=20)
    plt.axis([-4.5, 4.5, -0.2, 0.2])
    # 添加二阶变量后 线性可分"
    plt.subplot(122)
    plt.grid(True, which='both')
    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')
    plt.plot(X2D[:, 0][y == 0], X2D[:, 1][y == 0], "bs")
    plt.plot(X2D[:, 0][y == 1], X2D[:, 1][y == 1], "g^")
    plt.xlabel(r"$x_1$", fontsize=20)
    plt.ylabel(r"$x_2$", fontsize=20, rotation=0)
    plt.gca().get_yaxis().set_ticks([0, 4, 8, 12, 16])
    plt.plot([-4.5, 4.5], [6.5, 6.5], "r--", linewidth=3)
    plt.axis([-4.5, 4.5, -1, 17])
    plt.subplots_adjust(right=1)
    plt.show()
    # >>>>>>>>>>>>>>>>>>>>>>>>>> 添加多项式指标  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    X, y = make_moons(n_samples=100, noise=0.15, random_state=42)
    plot_dataset(X, y, [-1.5, 2.5, -1, 1.5])
    plt.show()
    polynomial_svm_clf = Pipeline([
        ("poly_features", PolynomialFeatures(degree=3)),
        ("scaler", StandardScaler()),
        ("svm_clf", LinearSVC(C=10, loss="hinge", random_state=42))
    ])
    polynomial_svm_clf.fit(X, y)
    plot_predictions(polynomial_svm_clf, [-1.5, 2.5, -1, 1.5])
    plot_dataset(X, y, [-1.5, 2.5, -1, 1.5])

    plt.show()
    # >>>>>>>>>>>>>>>>>>>>>>>>>> 使用多项式核  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # 使用三阶多项式的核
    poly_kernel_svm_clf = Pipeline([
        ("scaler", StandardScaler()),
        ("svm_clf", SVC(kernel="poly", degree=3, coef0=1, C=5))
    ])
    poly_kernel_svm_clf.fit(X, y)
    plt.figure(figsize=(11, 4))
    # 使用十阶多项式的核
    poly100_kernel_svm_clf = Pipeline([
        ("scaler", StandardScaler()),
        ("svm_clf", SVC(kernel="poly", degree=10, coef0=100, C=5))
    ])
    poly100_kernel_svm_clf.fit(X, y)

    plt.subplot(121)
    plot_predictions(poly_kernel_svm_clf, [-1.5, 2.5, -1, 1.5])
    plot_dataset(X, y, [-1.5, 2.5, -1, 1.5])
    plt.title(r"$d=3, r=1, C=5$", fontsize=18)

    plt.subplot(122)
    plot_predictions(poly100_kernel_svm_clf, [-1.5, 2.5, -1, 1.5])
    plot_dataset(X, y, [-1.5, 2.5, -1, 1.5])
    plt.title(r"$d=10, r=100, C=5$", fontsize=18)

    plt.show()


def gaussian_rbf(x, landmark, gamma):
    return np.exp(-gamma * np.linalg.norm(x - landmark, axis=1)**2)


def RBF_SVM():
    '''
    高斯RBF核函数SVM
    :return:
    '''
    X1D = np.linspace(-4, 4, 9).reshape(-1, 1)
    y = np.array([0, 0, 1, 1, 1, 1, 1, 0, 0])
    gamma = 0.3
    # 使用高斯核计算相似度作为新指标
    x1s = np.linspace(-4.5, 4.5, 200).reshape(-1, 1)
    x2s = gaussian_rbf(x1s, -2, gamma)
    x3s = gaussian_rbf(x1s, 1, gamma)
    # 获取转换后的数据
    XK = np.c_[gaussian_rbf(X1D, -2, gamma), gaussian_rbf(X1D, 1, gamma)]
    yk = np.array([0, 0, 1, 1, 1, 1, 1, 0, 0])

    plt.figure(figsize=(13, 4))
    # 绘制原始数据
    plt.subplot(121)
    plt.grid(True, which='both')
    plt.axhline(y=0, color='k')
    plt.scatter(x=[-2, 1], y=[0, 0], s=150, alpha=0.5, c="red")
    plt.plot(X1D[:, 0][yk == 0], np.zeros(4), "bs")
    plt.plot(X1D[:, 0][yk == 1], np.zeros(5), "g^")
    plt.plot(x1s, x2s, "g--")
    plt.plot(x1s, x3s, "b:")
    plt.gca().get_yaxis().set_ticks([0, 0.25, 0.5, 0.75, 1])
    plt.xlabel(r"$x_1$", fontsize=20)
    plt.ylabel(r"Similarity", fontsize=14)
    plt.annotate(r'$\mathbf{x}$',
                 xy=(X1D[3, 0], 0),
                 xytext=(-0.5, 0.20),
                 ha="center",
                 arrowprops=dict(facecolor='black', shrink=0.1),
                 fontsize=18,
                 )
    for i in range(len(X1D)):
        plt.text(X1D[i], 0.03, chr(i + 65))
    plt.text(-2, 0.9, "$x_2$", ha="center", fontsize=20)
    plt.text(1, 0.9, "$x_3$", ha="center", fontsize=20)
    plt.axis([-4.5, 4.5, -0.1, 1.1])
    # 绘制高斯核转换的数据
    plt.subplot(122)
    plt.grid(True, which='both')
    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')
    plt.plot(XK[:, 0][yk == 0], XK[:, 1][yk == 0], "bs")
    plt.plot(XK[:, 0][yk == 1], XK[:, 1][yk == 1], "g^")
    plt.xlabel(r"$x_2$", fontsize=20)
    plt.ylabel(r"$x_3$  ", fontsize=20, rotation=0)
    plt.annotate(r'$\phi\left(\mathbf{x}\right)$',
                 xy=(XK[3, 0], XK[3, 1]),
                 xytext=(0.65, 0.50),
                 ha="center",
                 arrowprops=dict(facecolor='black', shrink=0.1),
                 fontsize=18,
                 )
    for i in range(len(X1D)):
        plt.text(XK[i, 0] + 0.03, XK[i, 1] + 0.03, chr(i + 65))
    plt.plot([-0.1, 1.1], [0.57, -0.1], "r--", linewidth=3)
    plt.axis([-0.1, 1.1, -0.1, 1.1])

    plt.subplots_adjust(right=1)

    plt.show()

    x1_example = X1D[3, 0]
    for landmark in (-2, 1):
        k = gaussian_rbf(np.array([[x1_example]]), np.array([[landmark]]), gamma)
        print("Phi({}, {}) = {}".format(x1_example, landmark, k))
    # 使用RBF高斯核函数的SVM
    X, y = make_moons(n_samples=100, noise=0.15, random_state=42)

    rbf_kernel_svm_clf = Pipeline([
        ("scaler", StandardScaler()),
        ("svm_clf", SVC(kernel="rbf", gamma=5, C=0.001))
    ])
    rbf_kernel_svm_clf.fit(X, y)
    # 参数 gamma控制每个点的影响范围
    gamma1, gamma2 = 0.1, 5
    # C控制分割线宽度
    C1, C2 = 0.001, 1000
    hyperparams = (gamma1, C1), (gamma1, C2), (gamma2, C1), (gamma2, C2)
    # 尝试每一种参数组合
    svm_clfs = []
    for gamma, C in hyperparams:
        rbf_kernel_svm_clf = Pipeline([
            ("scaler", StandardScaler()),
            ("svm_clf", SVC(kernel="rbf", gamma=gamma, C=C))
        ])
        rbf_kernel_svm_clf.fit(X, y)
        svm_clfs.append(rbf_kernel_svm_clf)

    plt.figure(figsize=(11, 7))
    # 绘制图像
    for i, svm_clf in enumerate(svm_clfs):
        plt.subplot(221 + i)
        plot_predictions(svm_clf, [-1.5, 2.5, -1, 1.5])
        plot_dataset(X, y, [-1.5, 2.5, -1, 1.5])
        gamma, C = hyperparams[i]
        plt.title(r"$\gamma = {}, C = {}$".format(gamma, C), fontsize=16)

    plt.show()


def find_support_vectors(svm_reg, X, y):
    y_pred = svm_reg.predict(X)
    off_margin = (np.abs(y - y_pred) >= svm_reg.epsilon)
    return np.argwhere(off_margin)


def plot_svm_regression(svm_reg, X, y, axes):
    x1s = np.linspace(axes[0], axes[1], 100).reshape(100, 1)
    y_pred = svm_reg.predict(x1s)
    plt.plot(x1s, y_pred, "k-", linewidth=2, label=r"$\hat{y}$")
    plt.plot(x1s, y_pred + svm_reg.epsilon, "k--")
    plt.plot(x1s, y_pred - svm_reg.epsilon, "k--")
    plt.scatter(X[svm_reg.support_], y[svm_reg.support_], s=180, facecolors='#FFAAAA')
    plt.plot(X, y, "bo")
    plt.xlabel(r"$x_1$", fontsize=18)
    plt.legend(loc="upper left", fontsize=18)
    plt.axis(axes)


def Regression():
    '''
    SVM回归
    :return:
    '''
    np.random.seed(42)
    # 拟合线性数据
    m = 50
    X = 2 * np.random.rand(m, 1)
    y = (4 + 3 * X + np.random.randn(m, 1)).ravel()
    # 设置不同的间隔大小 epsilon
    svm_reg1 = LinearSVR(epsilon=1.5, random_state=42)
    svm_reg2 = LinearSVR(epsilon=0.5, random_state=42)
    svm_reg1.fit(X, y)
    svm_reg2.fit(X, y)
    # 训练数据
    svm_reg1.support_ = find_support_vectors(svm_reg1, X, y)
    svm_reg2.support_ = find_support_vectors(svm_reg2, X, y)

    eps_x1 = 1
    eps_y_pred = svm_reg1.predict([[eps_x1]])
    # 绘制大间隔回归拟合情况
    plt.figure(figsize=(9, 4))
    plt.subplot(121)
    plot_svm_regression(svm_reg1, X, y, [0, 2, 3, 11])
    plt.title(r"$\epsilon = {}$".format(svm_reg1.epsilon), fontsize=18)
    plt.ylabel(r"$y$", fontsize=18, rotation=0)
    # plt.plot([eps_x1, eps_x1], [eps_y_pred, eps_y_pred - svm_reg1.epsilon], "k-", linewidth=2)
    plt.annotate(
        '', xy=(eps_x1, eps_y_pred), xycoords='data',
        xytext=(eps_x1, eps_y_pred - svm_reg1.epsilon),
        textcoords='data', arrowprops={'arrowstyle': '<->', 'linewidth': 1.5}
    )
    plt.text(0.91, 5.6, r"$\epsilon$", fontsize=20)
    # 绘制小间隔回归拟合情况
    plt.subplot(122)
    plot_svm_regression(svm_reg2, X, y, [0, 2, 3, 11])
    plt.title(r"$\epsilon = {}$".format(svm_reg2.epsilon), fontsize=18)
    plt.show()
    # 拟合非线性数据
    np.random.seed(42)
    m = 100
    X = 2 * np.random.rand(m, 1) - 1
    y = (0.2 + 0.1 * X + 0.5 * X ** 2 + np.random.randn(m, 1) / 10).ravel()
    # 设置不同的间隔 C
    svm_poly_reg1 = SVR(kernel="poly", degree=2, C=100, epsilon=0.1, gamma="auto")
    svm_poly_reg2 = SVR(kernel="poly", degree=2, C=0.01, epsilon=0.1, gamma="auto")
    svm_poly_reg1.fit(X, y)
    svm_poly_reg2.fit(X, y)

    plt.figure(figsize=(9, 4))
    plt.subplot(121)
    plot_svm_regression(svm_poly_reg1, X, y, [-1, 1, 0, 1])
    plt.title(r"$degree={}, C={}, \epsilon = {}$".format(svm_poly_reg1.degree, svm_poly_reg1.C, svm_poly_reg1.epsilon),
              fontsize=18)
    plt.ylabel(r"$y$", fontsize=18, rotation=0)
    plt.subplot(122)
    plot_svm_regression(svm_poly_reg2, X, y, [-1, 1, 0, 1])
    plt.title(r"$degree={}, C={}, \epsilon = {}$".format(svm_poly_reg2.degree, svm_poly_reg2.C, svm_poly_reg2.epsilon),
              fontsize=18)
    plt.show()


class MyLinearSVC(BaseEstimator):
    def __init__(self, C=1, eta0=1, eta_d=10000, n_epochs=1000, random_state=None):
        self.C = C
        self.eta0 = eta0
        self.n_epochs = n_epochs
        self.random_state = random_state
        self.eta_d = eta_d

    def eta(self, epoch):
        return self.eta0 / (epoch + self.eta_d)

    def fit(self, X, y):
        # Random initialization
        if self.random_state:
            np.random.seed(self.random_state)
        w = np.random.randn(X.shape[1], 1)  # n feature weights
        b = 0
        m = len(X)
        y.resize(m, 1)
        t = y * 2 - 1  # -1 if t==0, +1 if t==1
        X_t = X * t
        self.Js = []

        # Training
        for epoch in range(self.n_epochs):
            support_vectors_idx = (X_t.dot(w) + t * b < 1).ravel()
            X_t_sv = X_t[support_vectors_idx]
            t_sv = t[support_vectors_idx]

            J = 1 / 2 * np.sum(w * w) + self.C * (np.sum(1 - X_t_sv.dot(w)) - b * np.sum(t_sv))
            self.Js.append(J)

            w_gradient_vector = w - self.C * np.sum(X_t_sv, axis=0).reshape(-1, 1)
            b_derivative = -self.C * np.sum(t_sv)

            w = w - self.eta(epoch) * w_gradient_vector
            b = b - self.eta(epoch) * b_derivative

        self.intercept_ = np.array([b])
        self.coef_ = np.array([w])
        support_vectors_idx = (X_t.dot(w) + t * b < 1).ravel()
        self.support_vectors_ = X[support_vectors_idx]
        return self

    def decision_function(self, X):
        return X.dot(self.coef_[0]) + self.intercept_[0]

    def predict(self, X):
        return (self.decision_function(X) >= 0).astype(np.float64)


def UseMyLineSVC():
    '''
    自定义SVM
    :return:
    '''
    # Training set
    iris = datasets.load_iris()
    X = iris["data"][:, (2, 3)]  # petal length, petal width
    y = (iris["target"] == 2).astype(np.float64).reshape(-1, 1)  # Iris-Virginica
    C = 2
    svm_clf = MyLinearSVC(C=C, eta0=10, eta_d=1000, n_epochs=60000, random_state=2)
    svm_clf.fit(X, y)
    svm_clf.predict(np.array([[5, 2], [4, 1]]))
    svm_clf2 = SVC(kernel="linear", C=C)
    svm_clf2.fit(X, y.ravel())
    # 绘制训练过程
    plt.plot(range(svm_clf.n_epochs), svm_clf.Js)
    plt.axis([0, svm_clf.n_epochs, 0, 100])
    plt.show()
    # 绘制训练结果
    yr = y.ravel()
    plt.figure(figsize=(12, 3.2))
    plt.subplot(121)
    plt.plot(X[:, 0][yr == 1], X[:, 1][yr == 1], "g^", label="Iris-Virginica")
    plt.plot(X[:, 0][yr == 0], X[:, 1][yr == 0], "bs", label="Not Iris-Virginica")
    plot_svc_decision_boundary(svm_clf, 4, 6)
    plt.xlabel("Petal length", fontsize=14)
    plt.ylabel("Petal width", fontsize=14)
    plt.title("MyLinearSVC", fontsize=14)
    plt.axis([4, 6, 0.8, 2.8])

    plt.subplot(122)
    plt.plot(X[:, 0][yr == 1], X[:, 1][yr == 1], "g^")
    plt.plot(X[:, 0][yr == 0], X[:, 1][yr == 0], "bs")
    plot_svc_decision_boundary(svm_clf2, 4, 6)
    plt.xlabel("Petal length", fontsize=14)
    plt.title("SVC", fontsize=14)
    plt.axis([4, 6, 0.8, 2.8])

    plt.show()


if __name__ == "__main__":
    # LinearClassify()
    # SoftLineClassify()
    # PolyomialClassify()
    # RBF_SVM()
    # Regression()
    UseMyLineSVC()
