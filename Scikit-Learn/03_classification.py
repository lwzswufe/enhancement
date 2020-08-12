# Common imports
import numpy as np
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_openml, load_files
from scipy.io import loadmat

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


def main():
    # mnist = fetch_openml('mnist_784', version=1, cache=True)
    # mnist = load_files("D:\\data\\mnist")
    # 读取本地数据
    mnist = loadmat("D:\\data\\mnist\\mldata\\mnist-original.mat")
    # mnist = load_files('D:\\data\\mnist\\mnist-original.mat')
    # fetch_openml() returns targets as strings
    # mnist.target = mnist.target.astype(np.int8)
    # fetch_openml() returns an unsorted dataset
    # sort_by_target(mnist)

    print(mnist["data"])

    print(mnist["label"])

    X, y = mnist["data"], mnist["label"]

    print("X.shape:", X.shape)
    print("y.shape:", y.shape)

    some_digit = X[:, 36000]
    some_digit_image = some_digit.reshape(28, 28)
    plt.imshow(some_digit_image, cmap=mpl.cm.binary,
               interpolation="nearest")
    plt.axis("off")

    plt.show()


if __name__ == "__main__":
    main()
