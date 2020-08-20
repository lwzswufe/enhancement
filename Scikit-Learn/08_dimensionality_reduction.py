# Common imports
import numpy as np
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d import Axes3D
from sklearn.datasets import make_swiss_roll
from matplotlib import gridspec
from six.moves import urllib
from scipy.io import loadmat
from sklearn.model_selection import train_test_split
from sklearn.decomposition import IncrementalPCA
from sklearn.decomposition import KernelPCA
from sklearn.manifold import LocallyLinearEmbedding
import time


class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)


def main():
    np.random.seed(4)
    m = 60
    w1, w2 = 0.1, 0.3
    noise = 0.1
    # 生成三维数据集
    angles = np.random.rand(m) * 3 * np.pi / 2 - 0.5
    X = np.empty((m, 3))
    X[:, 0] = np.cos(angles) + np.sin(angles) / 2 + noise * np.random.randn(m) / 2
    X[:, 1] = np.sin(angles) * 0.7 + noise * np.random.randn(m) / 2
    X[:, 2] = X[:, 0] * w1 + X[:, 1] * w2 + noise * np.random.randn(m)
    # 获取训练集主成分
    X_centered = X - X.mean(axis=0)
    U, s, Vt = np.linalg.svd(X_centered)
    # 提取前两个主成分
    c1 = Vt.T[:, 0]
    c2 = Vt.T[:, 1]
    print("主成分1:", c1)
    print("主成分2:", c2)
    m, n = X.shape

    S = np.zeros(X_centered.shape)
    S[:n, :n] = np.diag(s)

    np.allclose(X_centered, U.dot(S).dot(Vt))
    # 将数据转换到前两个主成分对应的平面上
    W2 = Vt.T[:, :2]
    X2D = X_centered.dot(W2)

    X2D_using_svd = X2D
    # 使用sklear库的PCA工具包
    # n_components 提取维度数
    pca = PCA(n_components=2)
    X2D = pca.fit_transform(X)
    print("主成分1:", pca.components_.T[:, 0])
    print("主成分2:", pca.components_.T[:, 1])
    print(X2D[:5])
    print(X2D[:5])
    # 比较两个array是不是每一元素都相等，默认在1e-05的误差范围内
    np.allclose(X2D, -X2D_using_svd)
    X3D_inv = pca.inverse_transform(X2D)
    np.allclose(X3D_inv, X)
    np.mean(np.sum(np.square(X3D_inv - X), axis=1))
    X3D_inv_using_svd = X2D_using_svd.dot(Vt[:2, :])
    np.allclose(X3D_inv_using_svd, X3D_inv - pca.mean_)

    print("每个轴的方差贡献度:", pca.explained_variance_ratio_)

    1 - pca.explained_variance_ratio_.sum()

    np.square(s) / np.square(s).sum()

    axes = [-1.8, 1.8, -1.3, 1.3, -1.0, 1.0]

    x1s = np.linspace(axes[0], axes[1], 10)
    x2s = np.linspace(axes[2], axes[3], 10)
    x1, x2 = np.meshgrid(x1s, x2s)

    C = pca.components_
    R = C.T.dot(C)
    z = (R[0, 2] * x1 + R[1, 2] * x2) / (1 - R[2, 2])
    # 绘制三维原始数据
    fig = plt.figure(figsize=(6, 3.8))
    ax = fig.add_subplot(111, projection='3d')

    X3D_above = X[X[:, 2] > X3D_inv[:, 2]]
    X3D_below = X[X[:, 2] <= X3D_inv[:, 2]]

    ax.plot(X3D_below[:, 0], X3D_below[:, 1], X3D_below[:, 2], "bo", alpha=0.5)

    ax.plot_surface(x1, x2, z, alpha=0.2, color="k")
    np.linalg.norm(C, axis=0)
    ax.add_artist(
        Arrow3D([0, C[0, 0]], [0, C[0, 1]], [0, C[0, 2]], mutation_scale=15, lw=1, arrowstyle="-|>", color="k"))
    ax.add_artist(
        Arrow3D([0, C[1, 0]], [0, C[1, 1]], [0, C[1, 2]], mutation_scale=15, lw=1, arrowstyle="-|>", color="k"))
    ax.plot([0], [0], [0], "k.")

    for i in range(m):
        if X[i, 2] > X3D_inv[i, 2]:
            ax.plot([X[i][0], X3D_inv[i][0]], [X[i][1], X3D_inv[i][1]], [X[i][2], X3D_inv[i][2]], "k-")
        else:
            ax.plot([X[i][0], X3D_inv[i][0]], [X[i][1], X3D_inv[i][1]], [X[i][2], X3D_inv[i][2]], "k-", color="#505050")

    ax.plot(X3D_inv[:, 0], X3D_inv[:, 1], X3D_inv[:, 2], "k+")
    ax.plot(X3D_inv[:, 0], X3D_inv[:, 1], X3D_inv[:, 2], "k.")
    ax.plot(X3D_above[:, 0], X3D_above[:, 1], X3D_above[:, 2], "bo")
    ax.set_xlabel("$x_1$", fontsize=18)
    ax.set_ylabel("$x_2$", fontsize=18)
    ax.set_zlabel("$x_3$", fontsize=18)
    ax.set_xlim(axes[0:2])
    ax.set_ylim(axes[2:4])
    ax.set_zlim(axes[4:6])

    plt.show()
    # 二维压缩后数据
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')

    ax.plot(X2D[:, 0], X2D[:, 1], "k+")
    ax.plot(X2D[:, 0], X2D[:, 1], "k.")
    ax.plot([0], [0], "ko")
    ax.arrow(0, 0, 0, 1, head_width=0.05, length_includes_head=True, head_length=0.1, fc='k', ec='k')
    ax.arrow(0, 0, 1, 0, head_width=0.05, length_includes_head=True, head_length=0.1, fc='k', ec='k')
    ax.set_xlabel("$z_1$", fontsize=18)
    ax.set_ylabel("$z_2$", fontsize=18, rotation=0)
    ax.axis([-1.5, 1.3, -1.2, 1.2])
    ax.grid(True)

    plt.show()
    # 瑞士卷数据
    X, t = make_swiss_roll(n_samples=1000, noise=0.2, random_state=42)
    axes = [-11.5, 14, -2, 23, -12, 15]

    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=t, cmap=plt.cm.hot)
    ax.view_init(10, -70)
    ax.set_xlabel("$x_1$", fontsize=18)
    ax.set_ylabel("$x_2$", fontsize=18)
    ax.set_zlabel("$x_3$", fontsize=18)
    ax.set_xlim(axes[0:2])
    ax.set_ylim(axes[2:4])
    ax.set_zlim(axes[4:6])

    plt.show()

    plt.figure(figsize=(11, 4))
    # 投影到平面
    plt.subplot(121)
    plt.scatter(X[:, 0], X[:, 1], c=t, cmap=plt.cm.hot)
    plt.axis(axes[:4])
    plt.xlabel("$x_1$", fontsize=18)
    plt.ylabel("$x_2$", fontsize=18, rotation=0)
    plt.grid(True)
    # 展开瑞士卷
    plt.subplot(122)
    plt.scatter(t, X[:, 1], c=t, cmap=plt.cm.hot)
    plt.axis([4, 15, axes[2], axes[3]])
    plt.xlabel("$z_1$", fontsize=18)
    plt.grid(True)

    plt.show()

    axes = [-11.5, 14, -2, 23, -12, 15]

    x2s = np.linspace(axes[2], axes[3], 10)
    x3s = np.linspace(axes[4], axes[5], 10)
    x2, x3 = np.meshgrid(x2s, x3s)
    # 在x轴上切割数据
    fig = plt.figure(figsize=(6, 5))
    ax = plt.subplot(111, projection='3d')

    positive_class = X[:, 0] > 5
    X_pos = X[positive_class]
    X_neg = X[~positive_class]
    ax.view_init(10, -70)
    ax.plot(X_neg[:, 0], X_neg[:, 1], X_neg[:, 2], "y^")
    ax.plot_wireframe(5, x2, x3, alpha=0.5)
    ax.plot(X_pos[:, 0], X_pos[:, 1], X_pos[:, 2], "gs")
    ax.set_xlabel("$x_1$", fontsize=18)
    ax.set_ylabel("$x_2$", fontsize=18)
    ax.set_zlabel("$x_3$", fontsize=18)
    ax.set_xlim(axes[0:2])
    ax.set_ylim(axes[2:4])
    ax.set_zlim(axes[4:6])

    plt.show()

    fig = plt.figure(figsize=(5, 4))
    ax = plt.subplot(111)

    plt.plot(t[positive_class], X[positive_class, 1], "gs")
    plt.plot(t[~positive_class], X[~positive_class, 1], "y^")
    plt.axis([4, 15, axes[2], axes[3]])
    plt.xlabel("$z_1$", fontsize=18)
    plt.ylabel("$z_2$", fontsize=18, rotation=0)
    plt.grid(True)

    plt.show()
    # 在y轴上切割数据
    fig = plt.figure(figsize=(6, 5))
    ax = plt.subplot(111, projection='3d')

    positive_class = 2 * (t[:] - 4) > X[:, 1]
    X_pos = X[positive_class]
    X_neg = X[~positive_class]
    ax.view_init(10, -70)
    ax.plot(X_neg[:, 0], X_neg[:, 1], X_neg[:, 2], "y^")
    ax.plot(X_pos[:, 0], X_pos[:, 1], X_pos[:, 2], "gs")
    ax.set_xlabel("$x_1$", fontsize=18)
    ax.set_ylabel("$x_2$", fontsize=18)
    ax.set_zlabel("$x_3$", fontsize=18)
    ax.set_xlim(axes[0:2])
    ax.set_ylim(axes[2:4])
    ax.set_zlim(axes[4:6])

    plt.show()

    fig = plt.figure(figsize=(5, 4))
    ax = plt.subplot(111)

    plt.plot(t[positive_class], X[positive_class, 1], "gs")
    plt.plot(t[~positive_class], X[~positive_class, 1], "y^")
    plt.plot([4, 15], [0, 22], "b-", linewidth=2)
    plt.axis([4, 15, axes[2], axes[3]])
    plt.xlabel("$z_1$", fontsize=18)
    plt.ylabel("$z_2$", fontsize=18, rotation=0)
    plt.grid(True)

    plt.show()


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


def plot_digits(instances, images_per_row=5, **options):
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


def PrincipalComponentAnalysis():
    angle = np.pi / 5
    stretch = 5
    m = 200

    np.random.seed(3)
    X = np.random.randn(m, 2) / 10
    X = X.dot(np.array([[stretch, 0], [0, 1]]))  # stretch
    X = X.dot([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]])  # rotate

    u1 = np.array([np.cos(angle), np.sin(angle)])
    u2 = np.array([np.cos(angle - 2 * np.pi / 6), np.sin(angle - 2 * np.pi / 6)])
    u3 = np.array([np.cos(angle - np.pi / 2), np.sin(angle - np.pi / 2)])

    X_proj1 = X.dot(u1.reshape(-1, 1))
    X_proj2 = X.dot(u2.reshape(-1, 1))
    X_proj3 = X.dot(u3.reshape(-1, 1))

    plt.figure(figsize=(8, 4))
    plt.subplot2grid((3, 2), (0, 0), rowspan=3)
    plt.plot([-1.4, 1.4], [-1.4 * u1[1] / u1[0], 1.4 * u1[1] / u1[0]], "k-", linewidth=1)
    plt.plot([-1.4, 1.4], [-1.4 * u2[1] / u2[0], 1.4 * u2[1] / u2[0]], "k--", linewidth=1)
    plt.plot([-1.4, 1.4], [-1.4 * u3[1] / u3[0], 1.4 * u3[1] / u3[0]], "k:", linewidth=2)
    plt.plot(X[:, 0], X[:, 1], "bo", alpha=0.5)
    plt.axis([-1.4, 1.4, -1.4, 1.4])
    plt.arrow(0, 0, u1[0], u1[1], head_width=0.1, linewidth=5, length_includes_head=True, head_length=0.1, fc='k',
              ec='k')
    plt.arrow(0, 0, u3[0], u3[1], head_width=0.1, linewidth=5, length_includes_head=True, head_length=0.1, fc='k',
              ec='k')
    plt.text(u1[0] + 0.1, u1[1] - 0.05, r"$\mathbf{c_1}$", fontsize=22)
    plt.text(u3[0] + 0.1, u3[1], r"$\mathbf{c_2}$", fontsize=22)
    plt.xlabel("$x_1$", fontsize=18)
    plt.ylabel("$x_2$", fontsize=18, rotation=0)
    plt.grid(True)

    plt.subplot2grid((3, 2), (0, 1))
    plt.plot([-2, 2], [0, 0], "k-", linewidth=1)
    plt.plot(X_proj1[:, 0], np.zeros(m), "bo", alpha=0.3)
    plt.gca().get_yaxis().set_ticks([])
    plt.gca().get_xaxis().set_ticklabels([])
    plt.axis([-2, 2, -1, 1])
    plt.grid(True)

    plt.subplot2grid((3, 2), (1, 1))
    plt.plot([-2, 2], [0, 0], "k--", linewidth=1)
    plt.plot(X_proj2[:, 0], np.zeros(m), "bo", alpha=0.3)
    plt.gca().get_yaxis().set_ticks([])
    plt.gca().get_xaxis().set_ticklabels([])
    plt.axis([-2, 2, -1, 1])
    plt.grid(True)

    plt.subplot2grid((3, 2), (2, 1))
    plt.plot([-2, 2], [0, 0], "k:", linewidth=2)
    plt.plot(X_proj3[:, 0], np.zeros(m), "bo", alpha=0.3)
    plt.gca().get_yaxis().set_ticks([])
    plt.axis([-2, 2, -1, 1])
    plt.xlabel("$z_1$", fontsize=18)
    plt.grid(True)

    plt.show()
    # 加载mnist数据
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    # 主成分分析
    pca = PCA()
    pca.fit(X_train)
    cumsum = np.cumsum(pca.explained_variance_ratio_)
    d = np.argmax(cumsum >= 0.95) + 1
    print("确保方差比大于95%需要至少{}个维度".format(d))

    pca = PCA(n_components=0.95)
    X_reduced = pca.fit_transform(X_train)
    print("方差比:", np.sum(pca.explained_variance_ratio_))

    pca = PCA(n_components=154)
    X_reduced = pca.fit_transform(X_train)
    X_recovered = pca.inverse_transform(X_reduced)
    # 压缩前数据
    plt.figure(figsize=(7, 4))
    plt.subplot(121)
    plot_digits(X_train[::2100])
    plt.title("Original", fontsize=16)
    # 压缩后数据
    plt.subplot(122)
    plot_digits(X_recovered[::2100])
    plt.title("Compressed", fontsize=16)

    plt.show()
    # 增量PCA
    n_batches = 100
    inc_pca = IncrementalPCA(n_components=154)
    for X_batch in np.array_split(X_train, n_batches):
        print(".", end="")  # not shown in the book
        inc_pca.partial_fit(X_batch)
    print("")
    X_reduced = inc_pca.transform(X_train)
    X_recovered_inc_pca = inc_pca.inverse_transform(X_reduced)

    plt.figure(figsize=(7, 4))
    plt.subplot(121)
    plot_digits(X_train[::2100])
    plt.subplot(122)
    plot_digits(X_recovered_inc_pca[::2100])
    plt.tight_layout()
    plt.show()
    # 随机PCA快速寻找主成分
    for n_components in (2, 10, 154):
        print("n_components =", n_components)
        regular_pca = PCA(n_components=n_components)
        inc_pca = IncrementalPCA(n_components=n_components, batch_size=500)
        rnd_pca = PCA(n_components=n_components, random_state=42, svd_solver="randomized")

        for pca in (regular_pca, inc_pca, rnd_pca):
            t1 = time.time()
            pca.fit(X_train)
            t2 = time.time()
            print("    {}: {:.1f} seconds".format(pca.__class__.__name__, t2 - t1))

    times_rpca = []
    times_pca = []
    sizes = [1000, 10000, 20000, 30000, 40000, 50000, 70000, 100000, 200000, 500000]
    for n_samples in sizes:
        X = np.random.randn(n_samples, 5)
        pca = PCA(n_components=2, svd_solver="randomized", random_state=42)
        t1 = time.time()
        pca.fit(X)
        t2 = time.time()
        times_rpca.append(t2 - t1)
        pca = PCA(n_components=2)
        t1 = time.time()
        pca.fit(X)
        t2 = time.time()
        times_pca.append(t2 - t1)

    plt.plot(sizes, times_rpca, "b-o", label="RPCA")
    plt.plot(sizes, times_pca, "r-s", label="PCA")
    plt.xlabel("n_samples")
    plt.ylabel("Training time")
    plt.legend(loc="upper left")
    plt.title("PCA and Randomized PCA time complexity ")
    plt.show()

    times_rpca = []
    times_pca = []
    sizes = [1000, 2000, 3000, 4000, 5000, 6000]
    for n_features in sizes:
        X = np.random.randn(2000, n_features)
        pca = PCA(n_components=2, random_state=42, svd_solver="randomized")
        t1 = time.time()
        pca.fit(X)
        t2 = time.time()
        times_rpca.append(t2 - t1)
        pca = PCA(n_components=2)
        t1 = time.time()
        pca.fit(X)
        t2 = time.time()
        times_pca.append(t2 - t1)

    plt.plot(sizes, times_rpca, "b-o", label="RPCA")
    plt.plot(sizes, times_pca, "r-s", label="PCA")
    plt.xlabel("n_features")
    plt.ylabel("Training time")
    plt.legend(loc="upper left")
    plt.title("PCA and Randomized PCA time complexity ")
    plt.show()


def KernalPrincipalComponentAnalysis():
    '''
    核主成分分析
    :return:
    '''
    X, t = make_swiss_roll(n_samples=1000, noise=0.2, random_state=42)

    lin_pca = KernelPCA(n_components=2, kernel="linear", fit_inverse_transform=True)
    rbf_pca = KernelPCA(n_components=2, kernel="rbf", gamma=0.0433, fit_inverse_transform=True)
    sig_pca = KernelPCA(n_components=2, kernel="sigmoid", gamma=0.001, coef0=1, fit_inverse_transform=True)

    y = t > 6.9

    plt.figure(figsize=(11, 4))
    for subplot, pca, title in ((131, lin_pca, "Linear kernel"), (132, rbf_pca, "RBF kernel, $\gamma=0.04$"),
                                (133, sig_pca, "Sigmoid kernel, $\gamma=10^{-3}, r=1$")):
        X_reduced = pca.fit_transform(X)
        if subplot == 132:
            X_reduced_rbf = X_reduced

        plt.subplot(subplot)
        # plt.plot(X_reduced[y, 0], X_reduced[y, 1], "gs")
        # plt.plot(X_reduced[~y, 0], X_reduced[~y, 1], "y^")
        plt.title(title, fontsize=14)
        plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=t, cmap=plt.cm.hot)
        plt.xlabel("$z_1$", fontsize=18)
        if subplot == 131:
            plt.ylabel("$z_2$", fontsize=18, rotation=0)
        plt.grid(True)

    plt.show()

    plt.figure(figsize=(6, 5))

    X_inverse = rbf_pca.inverse_transform(X_reduced_rbf)

    ax = plt.subplot(111, projection='3d')
    ax.view_init(10, -70)
    ax.scatter(X_inverse[:, 0], X_inverse[:, 1], X_inverse[:, 2], c=t, cmap=plt.cm.hot, marker="x")
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_zlabel("")
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])

    plt.show()

    X_reduced = rbf_pca.fit_transform(X)

    plt.figure(figsize=(11, 4))
    plt.subplot(132)
    plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=t, cmap=plt.cm.hot, marker="x")
    plt.xlabel("$z_1$", fontsize=18)
    plt.ylabel("$z_2$", fontsize=18, rotation=0)
    plt.grid(True)
    plt.show()
    # 压缩数据
    rbf_pca = KernelPCA(n_components=2, kernel="rbf", gamma=0.0433,
                        fit_inverse_transform=True)
    # 获取误差
    X_reduced = rbf_pca.fit_transform(X)
    # 重建原象
    X_preimage = rbf_pca.inverse_transform(X_reduced)


def LocallyLinearEmbed():
    '''
    线性局部嵌入
    :return:
    '''
    X, t = make_swiss_roll(n_samples=1000, noise=0.2, random_state=41)
    lle = LocallyLinearEmbedding(n_components=2, n_neighbors=10, random_state=42)
    X_reduced = lle.fit_transform(X)
    plt.title("Unrolled swiss roll using LLE", fontsize=14)
    plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=t, cmap=plt.cm.hot)
    plt.xlabel("$z_1$", fontsize=18)
    plt.ylabel("$z_2$", fontsize=18)
    plt.axis([-0.065, 0.055, -0.1, 0.12])
    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    # main()
    # PrincipalComponentAnalysis()
    # KernalPrincipalComponentAnalysis()
    LocallyLinearEmbed()