# Common imports
import numpy as np
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


# to make this notebook's output stable across runs
np.random.seed(42)


def LinearRegression():
    '''
    线性回归模型
    :return:
    '''
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
    m = len(X_b)
    plt.plot(X, y, "b.")
    n_iterations = 1000
    for iteration in range(n_iterations):
        if iteration < 10:
            y_predict = X_new_b.dot(theta)
            style = "b-" if iteration > 0 else "r--"
            plt.plot(X_new, y_predict, style)
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
    plt.subplot(131);
    plot_gradient_descent(X_b, X_new, X_new_b, X, y, theta, eta=0.02)
    plt.ylabel("$y$", rotation=0, fontsize=18)
    plt.subplot(132);
    plot_gradient_descent(X_b, X_new, X_new_b, X, y, theta, eta=0.1, theta_path=theta_path_bgd)
    plt.subplot(133);
    plot_gradient_descent(X_b, X_new, X_new_b, X, y, theta, eta=0.5)

    plt.show()


if __name__ == "__main__":
    # LinearRegression()
    LinearRegressionUsingGradientDescent()