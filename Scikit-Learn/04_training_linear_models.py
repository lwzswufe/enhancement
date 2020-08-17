# Common imports
import numpy as np
import numpy.random as rnd
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import LogisticRegression
from sklearn import datasets


def LinearRegressionModel():
    '''
    线性回归模型
    :return:
    '''
    np.random.seed(42)
    X = 2 * np.random.rand(100, 1)
    y = 4 + 3 * X + np.random.randn(100, 1)
    plt.plot(X, y, "b.")
    plt.xlabel("$x_1$", fontsize=18)
    plt.ylabel("$y$", rotation=0, fontsize=18)
    plt.axis([0, 2, 0, 15])
    plt.show()
    # 利用公式计算散点回归方程
    X_b = np.c_[np.ones((100, 1)), X]  # add x0 = 1 to each instance
    theta_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)
    # 计算得到回归方程参数
    print(theta_best)
    # 对数据进行预测 并作图
    X_new = np.array([[0], [2]])
    X_new_b = np.c_[np.ones((2, 1)), X_new]  # add x0 = 1 to each instance
    y_predict = X_new_b.dot(theta_best)
    print(y_predict)
    # 预测值作图
    plt.plot(X_new, y_predict, "r-")
    plt.plot(X, y, "b.")
    plt.axis([0, 2, 0, 15])
    plt.show()
    # 使用sklearn的线性回归模块
    lin_reg = LinearRegression()
    lin_reg.fit(X, y)
    # 回归方程参数
    print(lin_reg.intercept_)
    print(lin_reg.coef_)
    # 回归方程预测
    print(lin_reg.predict(X_new))


def plot_gradient_descent(X_b, X_new, X_new_b, X, y, theta, eta, theta_path=None):
    '''
    绘制梯度下降参数估计过程
    :param theta:
    :param eta:
    :param theta_path:
    :return:
    '''
    np.random.seed(42)
    m = len(X_b)
    plt.plot(X, y, "b.")
    n_iterations = 1000
    for iteration in range(n_iterations):
        # 绘制前10次迭代的过程
        if iteration < 10:
            y_predict = X_new_b.dot(theta)
            style = "b-" if iteration > 0 else "r--"
            plt.plot(X_new, y_predict, style)
        # 计算梯度
        gradients = 2/m * X_b.T.dot(X_b.dot(theta) - y)
        theta = theta - eta * gradients
        if theta_path is not None:
            theta_path.append(theta)
    plt.xlabel("$x_1$", fontsize=18)
    plt.axis([0, 2, 0, 15])
    plt.title(r"$\eta = {}$".format(eta), fontsize=16)


def LinearRegressionUsingGradientDescent():
    '''
    使用梯度下降法估计线性回归方程参数
    :return:
    '''
    np.random.seed(42)
    X = 2 * np.random.rand(100, 1)
    X_b = np.c_[np.ones((100, 1)), X]
    X_new = np.array([[0], [2]])
    X_new_b = np.c_[np.ones((2, 1)), X_new]
    y = 4 + 3 * X + np.random.randn(100, 1)
    eta = 0.1
    n_iterations = 1000
    m = 100
    theta = np.random.randn(2, 1)
    theta_path_bgd = []
    # 迭代估计参数
    for iteration in range(n_iterations):
        gradients = 2 / m * X_b.T.dot(X_b.dot(theta) - y)
        theta = theta - eta * gradients
    np.random.seed(42)
    theta = np.random.randn(2, 1)  # random initialization
    # 不同学习速率下回归方程参数学习
    plt.figure(figsize=(10, 4))
    plt.subplot(131)
    plot_gradient_descent(X_b, X_new, X_new_b, X, y, theta, eta=0.02)
    plt.ylabel("$y$", rotation=0, fontsize=18)
    plt.subplot(132)
    plot_gradient_descent(X_b, X_new, X_new_b, X, y, theta, eta=0.1, theta_path=theta_path_bgd)
    plt.subplot(133)
    plot_gradient_descent(X_b, X_new, X_new_b, X, y, theta, eta=0.5)

    plt.show()


def StochasticGradientDescent():
    '''
    随机梯度下降
    :return:
    '''
    np.random.seed(42)
    X = 2 * np.random.rand(100, 1)
    X_b = np.c_[np.ones((100, 1)), X]
    X_new = np.array([[0], [2]])
    X_new_b = np.c_[np.ones((2, 1)), X_new]
    y = 4 + 3 * X + np.random.randn(100, 1)
    theta_path_sgd = []
    m = len(X_b)
    n_epochs = 50
    t0, t1 = 5, 50  # learning schedule hyperparameters

    def learning_schedule(t):
        return t0 / (t + t1)
    # 初始化参数
    theta = np.random.randn(2, 1)  # random initialization
    # 训练迭代次数
    for epoch in range(n_epochs):
        # 针对对随机选择的样本进行训练
        for i in range(m):
            if epoch == 0 and i < 20:  # not shown in the book
                y_predict = X_new_b.dot(theta)  # not shown
                style = "b-" if i > 0 else "r--"  # not shown
                plt.plot(X_new, y_predict, style)  # not shown
            # 随机选择样本
            random_index = np.random.randint(m)
            xi = X_b[random_index:random_index + 1]
            yi = y[random_index:random_index + 1]
            # 计算梯度
            gradients = 2 * xi.T.dot(xi.dot(theta) - yi)
            eta = learning_schedule(epoch * m + i)
            # 参数学习
            theta = theta - eta * gradients
            theta_path_sgd.append(theta)  # not shown

    plt.plot(X, y, "b.")  # not shown
    plt.xlabel("$x_1$", fontsize=18)  # not shown
    plt.ylabel("$y$", rotation=0, fontsize=18)  # not shown
    plt.axis([0, 2, 0, 15])  # not shown
    plt.show()

    sgd_reg = SGDRegressor(max_iter=50, tol=-np.infty, penalty=None, eta0=0.1, random_state=42)
    sgd_reg.fit(X, y.ravel())
    print("SGD训练参数alpha:{} beta:{}".format(sgd_reg.intercept_, sgd_reg.coef_))
    # Mini-batch gradient descent
    # 小批量梯度下降
    theta_path_mgd = []

    n_iterations = 50
    minibatch_size = 20

    np.random.seed(42)
    theta = np.random.randn(2, 1)  # random initialization

    t0, t1 = 200, 1000

    def learning_schedule(t):
        return t0 / (t + t1)

    t = 0
    for epoch in range(n_iterations):
        shuffled_indices = np.random.permutation(m)
        X_b_shuffled = X_b[shuffled_indices]
        y_shuffled = y[shuffled_indices]
        # 每次训练选择minibatch_size个数据同时训练
        for i in range(0, m, minibatch_size):
            t += 1
            xi = X_b_shuffled[i:i + minibatch_size]
            yi = y_shuffled[i:i + minibatch_size]
            gradients = 2 / minibatch_size * xi.T.dot(xi.dot(theta) - yi)
            eta = learning_schedule(t)
            theta = theta - eta * gradients
            theta_path_mgd.append(theta)
    print("小批量梯度下降 训练参数:{}".format(theta))

    theta_path_sgd = np.array(theta_path_sgd)
    theta_path_mgd = np.array(theta_path_mgd)

    plt.figure(figsize=(7, 4))
    plt.plot(theta_path_sgd[:, 0], theta_path_sgd[:, 1], "r-s", linewidth=1, label="Stochastic")
    plt.plot(theta_path_mgd[:, 0], theta_path_mgd[:, 1], "g-+", linewidth=2, label="Mini-batch")
    plt.legend(loc="upper left", fontsize=16)
    plt.xlabel(r"$\theta_0$", fontsize=20)
    plt.ylabel(r"$\theta_1$   ", fontsize=20, rotation=0)
    plt.axis([2.5, 4.5, 2.3, 3.9])
    plt.show()


def PolynomialRegression():
    '''
    多项式回归
    :return:
    '''
    np.random.seed(42)
    m = 100
    X = 6 * np.random.rand(m, 1) - 3
    y = 0.5 * X ** 2 + X + 2 + np.random.randn(m, 1)
    plt.plot(X, y, "b.")
    plt.xlabel("$x_1$", fontsize=18)
    plt.ylabel("$y$", rotation=0, fontsize=18)
    plt.axis([-3, 3, 0, 10])
    plt.show()
    # 将X的二次方项作为新特征加入训练集
    poly_features = PolynomialFeatures(degree=2, include_bias=False)
    X_poly = poly_features.fit_transform(X)
    # 使用线性回归模型
    lin_reg = LinearRegression()
    lin_reg.fit(X_poly, y)
    print("y = {:.2f}x^2 + {:.2f}x + {:.2f} ".format(lin_reg.coef_[0][1], lin_reg.coef_[0][0], lin_reg.intercept_[0]))
    # 计算拟合曲线
    X_new = np.linspace(-3, 3, 100).reshape(100, 1)
    X_new_poly = poly_features.transform(X_new)
    y_new = lin_reg.predict(X_new_poly)
    # 绘图
    plt.plot(X, y, "b.")
    plt.plot(X_new, y_new, "r-", linewidth=2, label="Predictions")
    plt.xlabel("$x_1$", fontsize=18)
    plt.ylabel("$y$", rotation=0, fontsize=18)
    plt.legend(loc="upper left", fontsize=14)
    plt.axis([-3, 3, 0, 10])
    plt.show()
    # 300阶多项式
    for style, width, degree in (("g-", 1, 300), ("b--", 2, 2), ("r-+", 2, 1)):
        polybig_features = PolynomialFeatures(degree=degree, include_bias=False)
        std_scaler = StandardScaler()
        lin_reg = LinearRegression()
        polynomial_regression = Pipeline([
            ("poly_features", polybig_features),
            ("std_scaler", std_scaler),
            ("lin_reg", lin_reg),
        ])
        polynomial_regression.fit(X, y)
        y_newbig = polynomial_regression.predict(X_new)
        plt.plot(X_new, y_newbig, style, label=str(degree), linewidth=width)
    # 绘制拟合曲线
    plt.plot(X, y, "b.", linewidth=3)
    plt.legend(loc="upper left")
    plt.xlabel("$x_1$", fontsize=18)
    plt.ylabel("$y$", rotation=0, fontsize=18)
    plt.axis([-3, 3, 0, 10])
    plt.show()


def plot_learning_curves(model, X, y):
    '''
    绘制学习过程中平均误差的变化
    :param model:
    :param X:
    :param y:
    :return:
    '''
    # 划分训练集 验证集
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=10)
    train_errors, val_errors = [], []
    # 迭代训练
    for m in range(1, len(X_train)):
        model.fit(X_train[:m], y_train[:m])
        y_train_predict = model.predict(X_train[:m])
        y_val_predict = model.predict(X_val)
        # 记录每一代训练的误差
        train_errors.append(mean_squared_error(y_train[:m], y_train_predict))
        val_errors.append(mean_squared_error(y_val, y_val_predict))
    # 绘制误差图
    plt.plot(np.sqrt(train_errors), "r-+", linewidth=2, label="train")
    plt.plot(np.sqrt(val_errors), "b-", linewidth=3, label="val")
    plt.legend(loc="upper right", fontsize=14)  # not shown in the book
    plt.xlabel("Training set size", fontsize=14)  # not shown
    plt.ylabel("RMSE", fontsize=14)


def LearningProcess():
    np.random.seed(42)
    m = 100
    X = 6 * np.random.rand(m, 1) - 3
    y = 0.5 * X ** 2 + X + 2 + np.random.randn(m, 1)
    # 线性模型训练
    lin_reg = LinearRegression()
    plot_learning_curves(lin_reg, X, y)
    plt.axis([0, 80, 0, 3])  # not shown in the book
    plt.show()
    # 10阶模型训练
    polynomial_regression = Pipeline([
        ("poly_features", PolynomialFeatures(degree=10, include_bias=False)),
        ("lin_reg", LinearRegression()),
    ])
    plot_learning_curves(polynomial_regression, X, y)
    plt.axis([0, 80, 0, 3])  # not shown
    plt.show()


def plot_model(X, X_new, y, model_class, polynomial, alphas, **model_kargs):
    for alpha, style in zip(alphas, ("b-", "g--", "r:")):
        model = model_class(alpha, **model_kargs) if alpha > 0 else LinearRegression()
        if polynomial:
            model = Pipeline([
                ("poly_features", PolynomialFeatures(degree=10, include_bias=False)),
                ("std_scaler", StandardScaler()),
                ("regul_reg", model),
            ])
        model.fit(X, y)
        y_new_regul = model.predict(X_new)
        lw = 2 if alpha > 0 else 1
        plt.plot(X_new, y_new_regul, style, linewidth=lw, label=r"$\alpha = {}$".format(alpha))
    plt.plot(X, y, "b.", linewidth=3)
    plt.legend(loc="upper left", fontsize=15)
    plt.xlabel("$x_1$", fontsize=18)
    plt.axis([0, 3, 0, 4])


def RegularizedModels():
    '''
    正则化模型
    :return:
    '''
    np.random.seed(42)
    m = 20
    X = 3 * np.random.rand(m, 1)
    y = 1 + 0.5 * X + np.random.randn(m, 1) / 1.5
    X_new = np.linspace(0, 3, 100).reshape(100, 1)
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 岭回归模型 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    plt.figure(figsize=(8, 4))
    plt.subplot(121)
    plot_model(X, X_new, y, Ridge, polynomial=False, alphas=(0, 10, 100), random_state=42)
    plt.ylabel("$y$", rotation=0, fontsize=18)
    plt.subplot(122)
    plot_model(X, X_new, y, Ridge, polynomial=True, alphas=(0, 10 ** -5, 1), random_state=42)
    plt.show()
    # 在SGD上使用岭回归
    #  penalty="l2" 表示使用岭回归
    sgd_reg = SGDRegressor(max_iter=50, tol=-np.infty, penalty="l2", random_state=42)
    sgd_reg.fit(X, y.ravel())
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 套索回归模型Lasso <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    plt.figure(figsize=(8, 4))
    plt.subplot(121)
    plot_model(X, X_new, y, Lasso, polynomial=False, alphas=(0, 0.1, 1), random_state=42)
    plt.ylabel("$y$", rotation=0, fontsize=18)
    plt.subplot(122)
    plot_model(X, X_new, y, Lasso, polynomial=True, alphas=(0, 10 ** -7, 1), tol=1, random_state=42)
    plt.show()
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 弹性网络模型 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    elastic_net = ElasticNet(alpha=0.1, l1_ratio=0.5, random_state=42)
    elastic_net.fit(X, y)
    elastic_net.predict([[1.5]])


def bgd_path(theta, X, y, l1, l2, core = 1, eta = 0.1, n_iterations = 50):
    path = [theta]
    for iteration in range(n_iterations):
        gradients = core * 2/len(X) * X.T.dot(X.dot(theta) - y) + l1 * np.sign(theta) + 2 * l2 * theta

        theta = theta - eta * gradients
        path.append(theta)
    return np.array(path)


def EarlyStop():
    '''
    早期停止法
    :return:
    '''
    np.random.seed(42)
    m = 100
    X = 6 * np.random.rand(m, 1) - 3
    y = 2 + X + 0.5 * X ** 2 + np.random.randn(m, 1)

    X_train, X_val, y_train, y_val = train_test_split(X[:50], y[:50].ravel(), test_size=0.5, random_state=10)

    poly_scaler = Pipeline([
        ("poly_features", PolynomialFeatures(degree=90, include_bias=False)),
        ("std_scaler", StandardScaler()),
    ])

    X_train_poly_scaled = poly_scaler.fit_transform(X_train)
    X_val_poly_scaled = poly_scaler.transform(X_val)

    sgd_reg = SGDRegressor(max_iter=1,
                           tol=-np.infty,
                           penalty=None,
                           eta0=0.0005,
                           warm_start=True,
                           learning_rate="constant",
                           random_state=42)

    n_epochs = 500
    train_errors, val_errors = [], []
    for epoch in range(n_epochs):
        sgd_reg.fit(X_train_poly_scaled, y_train)
        y_train_predict = sgd_reg.predict(X_train_poly_scaled)
        y_val_predict = sgd_reg.predict(X_val_poly_scaled)
        train_errors.append(mean_squared_error(y_train, y_train_predict))
        val_errors.append(mean_squared_error(y_val, y_val_predict))
    # 寻找最优训练结果
    best_epoch = np.argmin(val_errors)
    best_val_rmse = np.sqrt(val_errors[best_epoch])

    plt.annotate('Best model',
                 xy=(best_epoch, best_val_rmse),
                 xytext=(best_epoch, best_val_rmse + 1),
                 ha="center",
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 fontsize=16,
                 )

    best_val_rmse -= 0.03  # just to make the graph look better
    plt.plot([0, n_epochs], [best_val_rmse, best_val_rmse], "k:", linewidth=2)
    plt.plot(np.sqrt(val_errors), "b-", linewidth=3, label="Validation set")
    plt.plot(np.sqrt(train_errors), "r--", linewidth=2, label="Training set")
    plt.legend(loc="upper right", fontsize=14)
    plt.xlabel("Epoch", fontsize=14)
    plt.ylabel("RMSE", fontsize=14)
    plt.show()
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>参数训练过程<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    t1a, t1b, t2a, t2b = -1, 3, -1.5, 1.5

    # ignoring bias term
    t1s = np.linspace(t1a, t1b, 500)
    t2s = np.linspace(t2a, t2b, 500)
    t1, t2 = np.meshgrid(t1s, t2s)
    T = np.c_[t1.ravel(), t2.ravel()]
    Xr = np.array([[-1, 1], [-0.3, -1], [1, 0.1]])
    yr = 2 * Xr[:, :1] + 0.5 * Xr[:, 1:]

    J = (1 / len(Xr) * np.sum((T.dot(Xr.T) - yr.T) ** 2, axis=1)).reshape(t1.shape)

    N1 = np.linalg.norm(T, ord=1, axis=1).reshape(t1.shape)
    N2 = np.linalg.norm(T, ord=2, axis=1).reshape(t1.shape)

    t_min_idx = np.unravel_index(np.argmin(J), J.shape)
    t1_min, t2_min = t1[t_min_idx], t2[t_min_idx]

    t_init = np.array([[0.25], [-1]])

    plt.figure(figsize=(12, 8))
    for i, N, l1, l2, title in ((0, N1, 0.5, 0, "Lasso"), (1, N2, 0, 0.1, "Ridge")):
        JR = J + l1 * N1 + l2 * N2 ** 2

        tr_min_idx = np.unravel_index(np.argmin(JR), JR.shape)
        t1r_min, t2r_min = t1[tr_min_idx], t2[tr_min_idx]

        levelsJ = (np.exp(np.linspace(0, 1, 20)) - 1) * (np.max(J) - np.min(J)) + np.min(J)
        levelsJR = (np.exp(np.linspace(0, 1, 20)) - 1) * (np.max(JR) - np.min(JR)) + np.min(JR)
        levelsN = np.linspace(0, np.max(N), 10)

        path_J = bgd_path(t_init, Xr, yr, l1=0, l2=0)
        path_JR = bgd_path(t_init, Xr, yr, l1, l2)
        path_N = bgd_path(t_init, Xr, yr, np.sign(l1) / 3, np.sign(l2), core=0)

        plt.subplot(221 + i * 2)
        plt.grid(True)
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.contourf(t1, t2, J, levels=levelsJ, alpha=0.9)
        plt.contour(t1, t2, N, levels=levelsN)
        plt.plot(path_J[:, 0], path_J[:, 1], "w-o")
        plt.plot(path_N[:, 0], path_N[:, 1], "y-^")
        plt.plot(t1_min, t2_min, "rs")
        plt.title(r"$\ell_{}$ penalty".format(i + 1), fontsize=16)
        plt.axis([t1a, t1b, t2a, t2b])
        if i == 1:
            plt.xlabel(r"$\theta_1$", fontsize=20)
        plt.ylabel(r"$\theta_2$", fontsize=20, rotation=0)

        plt.subplot(222 + i * 2)
        plt.grid(True)
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.contourf(t1, t2, JR, levels=levelsJR, alpha=0.9)
        plt.plot(path_JR[:, 0], path_JR[:, 1], "w-o")
        plt.plot(t1r_min, t2r_min, "rs")
        plt.title(title, fontsize=16)
        plt.axis([t1a, t1b, t2a, t2b])
        if i == 1:
            plt.xlabel(r"$\theta_1$", fontsize=20)

    plt.show()


def LogisticRegressionModel():
    '''
    逻辑回归
    :return:
    '''
    t = np.linspace(-10, 10, 100)
    sig = 1 / (1 + np.exp(-t))
    plt.figure(figsize=(9, 3))
    plt.plot([-10, 10], [0, 0], "k-")
    plt.plot([-10, 10], [0.5, 0.5], "k:")
    plt.plot([-10, 10], [1, 1], "k:")
    plt.plot([0, 0], [-1.1, 1.1], "k-")
    plt.plot(t, sig, "b-", linewidth=2, label=r"$\sigma(t) = \frac{1}{1 + e^{-t}}$")
    plt.xlabel("t")
    plt.legend(loc="upper left", fontsize=20)
    plt.axis([-10, 10, -0.1, 1.1])
    plt.show()
    # 加载鸢尾花数据集
    iris = datasets.load_iris()
    list(iris.keys())
    print(iris.DESCR)
    # 只针对花瓣宽度进行识别
    X = iris["data"][:, 3:]  # petal width
    y = (iris["target"] == 2).astype(np.int)  # 1 if Iris-Virginica, else 0
    log_reg = LogisticRegression(solver="liblinear", random_state=42)
    log_reg.fit(X, y)
    X_new = np.linspace(0, 3, 1000).reshape(-1, 1)
    y_proba = log_reg.predict_proba(X_new)

    plt.plot(X_new, y_proba[:, 1], "g-", linewidth=2, label="Iris-Virginica")
    plt.plot(X_new, y_proba[:, 0], "b--", linewidth=2, label="Not Iris-Virginica")

    X_new = np.linspace(0, 3, 1000).reshape(-1, 1)
    y_proba = log_reg.predict_proba(X_new)
    decision_boundary = X_new[y_proba[:, 1] >= 0.5][0]

    plt.figure(figsize=(8, 4))
    plt.plot(X[y == 0], y[y == 0], "bs")
    plt.plot(X[y == 1], y[y == 1], "g^")
    plt.plot([decision_boundary, decision_boundary], [-1, 2], "k:", linewidth=2)
    plt.plot(X_new, y_proba[:, 1], "g-", linewidth=2, label="Iris-Virginica")
    plt.plot(X_new, y_proba[:, 0], "b--", linewidth=2, label="Not Iris-Virginica")
    plt.text(decision_boundary + 0.02, 0.15, "Decision  boundary", fontsize=14, color="k", ha="center")
    plt.arrow(decision_boundary, 0.08, -0.3, 0, head_width=0.05, head_length=0.1, fc='b', ec='b')
    plt.arrow(decision_boundary, 0.92, 0.3, 0, head_width=0.05, head_length=0.1, fc='g', ec='g')
    plt.xlabel("Petal width (cm)", fontsize=14)
    plt.ylabel("Probability", fontsize=14)
    plt.legend(loc="center left", fontsize=14)
    plt.axis([0, 3, -0.02, 1.02])
    plt.show()
    # 只针对花瓣宽度 与花瓣长度进行识别
    X = iris["data"][:, (2, 3)]  # petal length, petal width
    y = (iris["target"] == 2).astype(np.int)

    log_reg = LogisticRegression(solver="liblinear", C=10 ** 10, random_state=42)
    log_reg.fit(X, y)

    x0, x1 = np.meshgrid(
        np.linspace(2.9, 7, 500).reshape(-1, 1),
        np.linspace(0.8, 2.7, 200).reshape(-1, 1),
    )
    X_new = np.c_[x0.ravel(), x1.ravel()]

    y_proba = log_reg.predict_proba(X_new)

    plt.figure(figsize=(10, 4))
    plt.plot(X[y == 0, 0], X[y == 0, 1], "bs")
    plt.plot(X[y == 1, 0], X[y == 1, 1], "g^")

    zz = y_proba[:, 1].reshape(x0.shape)
    contour = plt.contour(x0, x1, zz, cmap=plt.cm.brg)

    left_right = np.array([2.9, 7])
    boundary = -(log_reg.coef_[0][0] * left_right + log_reg.intercept_[0]) / log_reg.coef_[0][1]

    plt.clabel(contour, inline=1, fontsize=12)
    plt.plot(left_right, boundary, "k--", linewidth=3)
    plt.text(3.5, 1.5, "Not Iris-Virginica", fontsize=14, color="b", ha="center")
    plt.text(6.5, 2.3, "Iris-Virginica", fontsize=14, color="g", ha="center")
    plt.xlabel("Petal length", fontsize=14)
    plt.ylabel("Petal width", fontsize=14)
    plt.axis([2.9, 7, 0.8, 2.7])
    plt.show()


def SoftmaxModel():
    '''
    多元逻辑回归
    :return:
    '''
    iris = datasets.load_iris()
    list(iris.keys())
    print(iris.DESCR)
    X = iris["data"][:, (2, 3)]  # petal length, petal width
    y = iris["target"]

    softmax_reg = LogisticRegression(multi_class="multinomial", solver="lbfgs", C=10, random_state=42)
    softmax_reg.fit(X, y)

    x0, x1 = np.meshgrid(
        np.linspace(0, 8, 500).reshape(-1, 1),
        np.linspace(0, 3.5, 200).reshape(-1, 1),
    )
    X_new = np.c_[x0.ravel(), x1.ravel()]

    y_proba = softmax_reg.predict_proba(X_new)
    y_predict = softmax_reg.predict(X_new)

    zz1 = y_proba[:, 1].reshape(x0.shape)
    zz = y_predict.reshape(x0.shape)

    plt.figure(figsize=(10, 4))
    plt.plot(X[y == 2, 0], X[y == 2, 1], "g^", label="Iris-Virginica")
    plt.plot(X[y == 1, 0], X[y == 1, 1], "bs", label="Iris-Versicolor")
    plt.plot(X[y == 0, 0], X[y == 0, 1], "yo", label="Iris-Setosa")

    from matplotlib.colors import ListedColormap
    custom_cmap = ListedColormap(['#fafab0', '#9898ff', '#a0faa0'])

    plt.contourf(x0, x1, zz, cmap=custom_cmap)
    contour = plt.contour(x0, x1, zz1, cmap=plt.cm.brg)
    plt.clabel(contour, inline=1, fontsize=12)
    plt.xlabel("Petal length", fontsize=14)
    plt.ylabel("Petal width", fontsize=14)
    plt.legend(loc="center left", fontsize=14)
    plt.axis([0, 7, 0, 3.5])
    plt.show()


if __name__ == "__main__":
    # LinearRegressionModel()
    # LinearRegressionUsingGradientDescent()
    # StochasticGradientDescent()
    # PolynomialRegression()
    # LearningProcess()
    # RegularizedModels()
    # EarlyStop()
    # LogisticRegressionModel()
    SoftmaxModel()
