import matplotlib
import matplotlib.pyplot as plt
from tensorflow.compat import v1 as tf
from tensorflow import random as tf_rnd
import tensorboard
# import tensorflow as tf
from datetime import datetime
import numpy as np
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
HOUSING_PATH = os.path.join("datasets", "housing")


def load_housing_data(housing_path=HOUSING_PATH):
    '''
    加载数据
    :param housing_path:
    :return:
    '''
    csv_path = os.path.join(housing_path, "housing.csv")
    return pd.read_csv(csv_path)


housing = load_housing_data()
housing.fillna(0, inplace=True)
Y = housing["median_house_value"].to_numpy().reshape((-1, 1))
Y = Y / np.mean(Y)
data = housing.to_numpy()
data = data[:, :data.shape[1] - 2]
m, n = data.shape
# 添加一列常数项
housing_data_plus_bias = np.c_[np.ones((m, 1)), data]
n_batches = 1

scaler = StandardScaler()
scaled_housing_data = scaler.fit_transform(data)
scaled_housing_data_plus_bias = np.c_[np.ones((m, 1)), scaled_housing_data]


def reset_graph(seed=42):
    '''
    重置计算图
    :param seed:
    :return:
    '''
    tf.reset_default_graph()
    tf.set_random_seed(seed)
    np.random.seed(seed)


def fetch_batch(epoch, batch_index, batch_size):
    np.random.seed(epoch * n_batches + batch_index)   # not shown in the book
    indices = np.random.randint(m, size=batch_size)   # not shown
    X_batch = scaled_housing_data_plus_bias[indices]  # not shown
    y_batch = Y[indices]  # not shown
    return X_batch, y_batch


def main():
    reset_graph()
    now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    root_logdir = "tf_logs"
    logdir = "{}/run-{}/".format(root_logdir, now)

    learning_rate = 0.02
    # 创建占位符节点 用于传入/传出数据
    X = tf.placeholder(tf.float32, shape=(None, n + 1), name="X")
    y = tf.placeholder(tf.float32, shape=(None, 1), name="y")
    # 创建参数节点
    theta = tf.Variable(tf_rnd.uniform([n + 1, 1], -1.0, 1.0, seed=42), name="theta")
    # 创建一个边/张量
    y_pred = tf.matmul(X, theta, name="predictions")
    # 定义误差
    error = y_pred - y
    mse = tf.reduce_mean(tf.square(error), name="mse")
    # 使用优化器
    # optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
    optimizer = tf.train.MomentumOptimizer(learning_rate=learning_rate, momentum=0.9)
    # 为优化器指定目标
    training_op = optimizer.minimize(mse)
    # 变量初始化
    init = tf.global_variables_initializer()
    # 定义可视化数据保存的位置
    mse_summary = tf.summary.scalar('MSE', mse)
    file_writer = tf.summary.FileWriter(logdir, tf.get_default_graph())

    n_epochs = 1000
    batch_size = 100
    n_batches = int(np.ceil(m / batch_size))

    with tf.Session() as sess:  # not shown in the book
        sess.run(init)  # not shown
        for epoch in range(n_epochs):  # not shown
            for batch_index in range(n_batches):

                X_batch, y_batch = fetch_batch(epoch, batch_index, batch_size)
                # 定期输出训练状态
                if batch_index % 10 == 0:
                    summary_str = mse_summary.eval(feed_dict={X: X_batch, y: y_batch})
                    step = epoch * n_batches + batch_index
                    file_writer.add_summary(summary_str, step)
                # 执行训练
                sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
            # 输出训练误差
            if epoch % 10 == 9:
                print("Epoch:", epoch + 1, "MSE =", mse.eval(feed_dict={X: X_batch, y: y_batch}))
                # print("Epoch:", epoch, "theta=", theta.eval().T)
                # print("Epoch:", epoch, "y_pred=", y_pred.eval(feed_dict={X: X_batch, y: y_batch}).T)
            # print("best_theta:",  theta.eval())
        best_theta = theta.eval()

    # 关闭可视化数据保存器
    file_writer.close()
    # show_graph(tf.get_default_graph())


'''
可视化命令 
打开cmd运行
C:\\Anaconda3\\Scripts\\tensorboard.exe --logdir D:\\Code\\Code\\enhancement\\Scikit-Learn\\tf_logs
然后再浏览器访问
http://localhost:6006
'''


if __name__ == "__main__":
    main()
