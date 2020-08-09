# Common imports
import numpy as np
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tarfile
from six.moves import urllib
import pandas as pd
from pandas.plotting import scatter_matrix
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import FeatureUnion
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint
# to make this notebook's output stable across runs
np.random.seed(42)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>获取数据<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"
HOUSING_PATH = os.path.join("datasets", "housing")
HOUSING_URL = DOWNLOAD_ROOT + "datasets/housing/housing.tgz"
# Where to save the figures
PROJECT_ROOT_DIR = "."
CHAPTER_ID = "end_to_end_project"
IMAGES_PATH = os.path.join(PROJECT_ROOT_DIR, "images", CHAPTER_ID)


def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)


def fetch_housing_data(housing_url=HOUSING_URL, housing_path=HOUSING_PATH):
    '''
    下载房屋数据
    :param housing_url:
    :param housing_path:
    :return:
    '''
    # 创建文件夹
    os.makedirs(housing_path, exist_ok=True)
    # 生成压缩文件夹名称
    tgz_path = os.path.join(housing_path, "housing.tgz")
    # 下载数据
    urllib.request.urlretrieve(housing_url, tgz_path)
    # 解压数据
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path=housing_path)
    housing_tgz.close()


def load_housing_data(housing_path=HOUSING_PATH):
    '''
    加载数据
    :param housing_path:
    :return:
    '''
    csv_path = os.path.join(housing_path, "housing.csv")
    return pd.read_csv(csv_path)


# For illustration only. Sklearn has train_test_split()
def split_train_test(df=pd.DataFrame(), test_ratio=0.2):
    '''
    创建测试集
    :param data:
    :param test_ratio:
    :return:
    '''
    df_test = df.sample(frac=test_ratio, replace=True)
    df_train = df.sample(frac=1-test_ratio, replace=True)
    return df_test, df_train


def main():
    # 下载数据
    # fetch_housing_data()
    # 读取数据
    housing = load_housing_data()
    print("数据前5行：")
    print(housing.head())
    print("数据表数据信息：")
    print(housing.info())
    print("查看分类变量分布信息：")
    print(housing["ocean_proximity"].value_counts())
    print("简要描述统计：")
    print(housing.describe())
    # 数据分布可视化
    housing.hist(bins=50, figsize=(20, 15))
    plt.show()

    train_set, test_set = split_train_test(housing, 0.2)
    print("train:{}  test:{} total:{}".format(len(train_set), len(test_set), len(housing)))
    # 连续变量分组
    housing["income_cat"] = pd.cut(housing["median_income"],
                                   bins=[0., 1.5, 3.0, 4.5, 6., np.inf],
                                   labels=[1, 2, 3, 4, 5])
    print("查看分组变量分布信息：")
    print(housing["income_cat"].value_counts())
    print("查看分组变量分布信息(比例)：")
    print(housing["income_cat"].value_counts() / len(housing))
    housing["income_cat"].hist()
    plt.show()
    # 删除分组数据
    housing.drop("income_cat", axis=1, inplace=True)
    # 数据可视化
    housing.plot(kind="scatter", x="longitude", y="latitude")
    plt.show()
    # 弱化每个点的色彩浓度
    housing.plot(kind="scatter", x="longitude", y="latitude", alpha=0.1)
    plt.show()
    # 为每个点添加颜色信息 定制每个点的颜色
    # 圆点大小  s
    # 每个点的颜色 c
    housing.plot(kind="scatter", x="longitude", y="latitude", alpha=0.4,
                 s=housing["population"] / 100, label="population", figsize=(10, 7),
                 c="median_house_value", cmap=plt.get_cmap("jet"), colorbar=True,
                 sharex=False)
    plt.legend()
    plt.show()

    california_img = mpimg.imread(PROJECT_ROOT_DIR + '/images/end_to_end_project/california.png')
    ax = housing.plot(kind="scatter", x="longitude", y="latitude", figsize=(10, 7),
                      s=housing['population'] / 100, label="Population",
                      c="median_house_value", cmap=plt.get_cmap("jet"),
                      colorbar=False, alpha=0.4,
                      )
    # 设置坐标轴范围
    plt.imshow(california_img, extent=[-124.55, -113.80, 32.45, 42.05], alpha=0.5,
               cmap=plt.get_cmap("jet"))
    plt.ylabel("Latitude", fontsize=14)
    plt.xlabel("Longitude", fontsize=14)

    prices = housing["median_house_value"]
    tick_values = np.linspace(prices.min(), prices.max(), 11)
    # 色彩bar
    cbar = plt.colorbar()
    # 设置坐标轴刻度
    cbar.ax.set_yticklabels(["$%dk" % (round(v / 1000)) for v in tick_values], fontsize=14)
    cbar.set_label('Median House Value', fontsize=16)
    # 图例
    plt.legend(fontsize=16)
    save_fig("california_housing_prices_plot")
    plt.show()
    # 计算相关性
    corr_matrix = housing.corr()
    print("房屋中位数价格 与其他因素的相关性")
    print(corr_matrix["median_house_value"].sort_values(ascending=False))
    # 绘制数据集各个指标之间的相关性图
    attributes = ["median_house_value", "median_income", "total_rooms",
                  "housing_median_age"]
    scatter_matrix(housing[attributes], figsize=(12, 8))
    plt.show()
    # 绘制两个指标之间的相关性图
    housing.plot(kind="scatter", x="median_income", y="median_house_value",
                 alpha=0.1)
    plt.axis([0, 16, 0, 550000])
    save_fig("income_vs_house_value_scatterplot")
    # 生成衍生指标
    housing["rooms_per_household"] = housing["total_rooms"] / housing["households"]
    housing["bedrooms_per_room"] = housing["total_bedrooms"] / housing["total_rooms"]
    housing["population_per_household"] = housing["population"] / housing["households"]
    #
    corr_matrix = housing.corr()
    print("衍生股票和房价中位数之间的关系")
    print(corr_matrix["median_house_value"].sort_values(ascending=False))
    #
    housing.plot(kind="scatter", x="rooms_per_household", y="median_house_value",
                 alpha=0.2)
    plt.axis([0, 5, 0, 520000])
    plt.show()
    # 绘制相关性图
    housing.plot(kind="scatter", x="rooms_per_household", y="median_house_value",
                 alpha=0.2)
    plt.axis([0, 5, 0, 520000])
    plt.show()
    # 输出描述信息统计
    print("描述信息统计")
    print(housing.describe())


rooms_ix = 3
bedrooms_ix = 4
population_ix = 5
household_ix = 6


class CombinedAttributesAdder(BaseEstimator, TransformerMixin):

    def __init__(self, add_bedrooms_per_room = True): # no *args or **kwargs
        self.add_bedrooms_per_room = add_bedrooms_per_room

    def fit(self, X, y=None):
        return self  # nothing else to do

    def transform(self, X, y=None):
        rooms_per_household = X[:, rooms_ix] / X[:, household_ix]
        population_per_household = X[:, population_ix] / X[:, household_ix]
        if self.add_bedrooms_per_room:
            bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]
            return np.c_[X, rooms_per_household, population_per_household,
                         bedrooms_per_room]
        else:
            return np.c_[X, rooms_per_household, population_per_household]


def add_extra_features(X, add_bedrooms_per_room=True):
    rooms_per_household = X[:, rooms_ix] / X[:, household_ix]
    population_per_household = X[:, population_ix] / X[:, household_ix]
    if add_bedrooms_per_room:
        bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]
        return np.c_[X, rooms_per_household, population_per_household,
                     bedrooms_per_room]
    else:
        return np.c_[X, rooms_per_household, population_per_household]


def data_clean():
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 数据清理 <<<<<<<<<<<<<<<<<<<<<<<<<<<<

    housing = load_housing_data()
    # 设定用中位数填充缺失值
    imputer = SimpleImputer(strategy="median")
    # 删掉分类属性的数据 保留定序数据
    housing_num = housing.drop('ocean_proximity', axis=1)
    # impoter适配训练集
    imputer.fit(housing_num)
    # SimpleImputer(copy=True, fill_value=None, missing_values=np.nan,
    #               strategy='median', verbose=0)
    # 转换为numpy数组
    X = imputer.transform(housing_num)
    # 转回DataFrame
    housing_tr = pd.DataFrame(X, columns=housing_num.columns)
    # >>>>>>>>>>>>>>>>>>>>>>>>>将分类特征编码为整数数组<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # 该转换器的输入应为整数或字符串之类的数组，表示分类（离散）特征所采用的值。
    ordinal_encoder = OrdinalEncoder()
    housing_cat = housing[['ocean_proximity']]
    print(housing_cat.head(10))
    housing_cat_encoded = ordinal_encoder.fit_transform(housing_cat)
    print(housing_cat_encoded[:10])
    # >>>>>>>>>>>>>>>>>>>>>>>>>将分类特征编码为独热向量数组<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    cat_encoder = OneHotEncoder()
    housing_cat_1hot = cat_encoder.fit_transform(housing_cat)
    print(housing_cat_1hot.toarray()[:10])
    print(cat_encoder.categories_)
    # >>>>>>>>>>>>>>>>>>>>>>>>>自定义转换器<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # 实现自动生成衍生指标
    # get the right column indices: safer than hard-coding indices 3, 4, 5, 6
    print(housing.columns)
    attr_adder = CombinedAttributesAdder(add_bedrooms_per_room=False)
    housing_extra_attribs = attr_adder.transform(housing.values)
    # 使用函数的模式
    attr_adder = FunctionTransformer(add_extra_features, validate=False,
                                     kw_args={"add_bedrooms_per_room": False})
    housing_extra_attribs = attr_adder.fit_transform(housing.values)
    # 数据转回DataFrame
    housing_extra_attribs = pd.DataFrame(
        housing_extra_attribs,
        columns=list(housing.columns) + ["rooms_per_household", "population_per_household"],
        index=housing.index)
    print(housing_extra_attribs.head())


# Create a class to select numerical or categorical columns
class OldDataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.attribute_names].values


def pipline():
    '''
    流水线处理数据
    :return:
    '''
    # 数据读取
    housing = load_housing_data()
    # 删掉分类属性的数据 保留定序数据
    # housing_num = housing.drop('ocean_proximity', axis=1)
    # 创建流水线
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy="median")),
        ('attribs_adder', FunctionTransformer(add_extra_features, validate=False)),
        ('std_scaler', StandardScaler()),
    ])
    # housing_num_tr = num_pipeline.fit_transform(housing_num)
    # print(housing_num_tr)
    # 分开处理数值类型  标签类型数据
    num_attribs = list(housing.columns)
    cat_attribs = ["ocean_proximity"]
    # 删除目标变量
    num_attribs.remove("median_house_value")
    # 删除标签类型变量
    for col in cat_attribs:
        num_attribs.remove(col)

    full_pipeline = ColumnTransformer([
        ("num", num_pipeline, num_attribs),
        ("cat", OneHotEncoder(), cat_attribs),
    ])

    housing_prepared = full_pipeline.fit_transform(housing)
    housing_labels = housing["median_house_value"].copy()
    return housing_prepared, housing_labels


def pipline2():
    # 数据读取
    housing = load_housing_data()
    # 删掉分类属性的数据 保留定序数据
    housing_num = housing.drop('ocean_proximity', axis=1)
    num_attribs = list(housing_num)
    cat_attribs = ["ocean_proximity"]
    # 数值类型数据处理流水线
    old_num_pipeline = Pipeline([
        ('selector', OldDataFrameSelector(num_attribs)),
        ('imputer', SimpleImputer(strategy="median")),
        ('attribs_adder', FunctionTransformer(add_extra_features, validate=False)),
        ('std_scaler', StandardScaler()),
    ])
    # 标签类型数据处理流水线
    old_cat_pipeline = Pipeline([
        ('selector', OldDataFrameSelector(cat_attribs)),
        ('cat_encoder', OneHotEncoder(sparse=False)),
    ])
    # 整合流水线
    old_full_pipeline = FeatureUnion(transformer_list=[
        ("num_pipeline", old_num_pipeline),
        ("cat_pipeline", old_cat_pipeline),
    ])
    # 准备数据
    old_housing_prepared = old_full_pipeline.fit_transform(housing)
    print(old_housing_prepared)


def display_scores(scores):
    print("Scores:", scores)
    print("Mean:", scores.mean())
    print("Standard deviation:", scores.std())


def linear_model(housing_prepared, housing_labels):
    '''
    线性模型
    :param housing_prepared:  训练数据
    :param housing_labels:    目标
    :return:
    '''
    lin_reg = LinearRegression()
    lin_reg.fit(housing_prepared, housing_labels)
    LinearRegression(copy_X=True, fit_intercept=True, n_jobs=None,
                     normalize=False)
    predict = lin_reg.predict(housing_prepared[:5])
    print("   label     Predictions")
    for i in range(5):
        print("{:.3f}, {:.3f}".format(housing_labels[i], predict[i]))


def dtr(housing_prepared, housing_labels):
    '''
    决策树
    :param housing_prepared:  训练数据
    :param housing_labels:    目标
    :return:
    '''
    tree_reg = DecisionTreeRegressor(random_state=42)
    tree_reg.fit(housing_prepared, housing_labels)

    DecisionTreeRegressor(criterion='mse', max_depth=None, max_features=None,
                          max_leaf_nodes=None, min_impurity_decrease=0.0,
                          min_impurity_split=None, min_samples_leaf=1,
                          min_samples_split=2, min_weight_fraction_leaf=0.0,
                          presort=False, random_state=42, splitter='best')
    housing_predictions = tree_reg.predict(housing_prepared)
    tree_mse = mean_squared_error(housing_labels, housing_predictions)
    tree_rmse = np.sqrt(tree_mse)
    print("   label     Predictions")
    for i in range(5):
        print("{:.3f}, {:.3f}".format(housing_labels[i], housing_predictions[i]))
    print("dtr mse: {:.3f}".format(tree_rmse))
    # 分组交叉验证
    # cv随即分割组数
    scores = cross_val_score(tree_reg, housing_prepared, housing_labels,
                             scoring="neg_mean_squared_error", cv=10)
    tree_rmse_scores = np.sqrt(-scores)
    display_scores(tree_rmse_scores)
    # 随机森林
    forest_reg = RandomForestRegressor(n_estimators=10, random_state=42)
    forest_reg.fit(housing_prepared, housing_labels)
    housing_predictions = forest_reg.predict(housing_prepared)
    forest_mse = mean_squared_error(housing_labels, housing_predictions)
    forest_rmse = np.sqrt(forest_mse)
    print("RandomForest MSE:{:.3F}".format(forest_rmse))
    forest_scores = cross_val_score(forest_reg, housing_prepared, housing_labels,
                                    scoring="neg_mean_squared_error", cv=10)
    forest_rmse_scores = np.sqrt(-forest_scores)
    display_scores(forest_rmse_scores)
    # 参数网格搜索
    # 设置搜索范围
    param_grid = [
        # try 12 (3×4) combinations of hyperparameters
        {'n_estimators': [3, 10, 30], 'max_features': [2, 4, 6, 8]},
        # then try 6 (2×3) combinations with bootstrap set as False
        {'bootstrap': [False], 'n_estimators': [3, 10], 'max_features': [2, 3, 4]},
    ]
    forest_reg = RandomForestRegressor(random_state=42)
    # train across 5 folds, that's a total of (12+6)*5=90 rounds of training
    grid_search = GridSearchCV(forest_reg, param_grid, cv=5,
                               scoring='neg_mean_squared_error', return_train_score=True)
    grid_search.fit(housing_prepared, housing_labels)
    print("best_params:{}".format(grid_search.best_params_))
    print("best_estimator:{}".format(grid_search.best_estimator_))
    # 输出每一个树的得分与参数
    cvres = grid_search.cv_results_
    for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
        print(np.sqrt(-mean_score), params)
    print(pd.DataFrame(grid_search.cv_results_))

    # 参数随机搜索
    # 设置随机搜索参数范围
    param_distribs = {
        'n_estimators': randint(low=1, high=200),
        'max_features': randint(low=1, high=8),
    }

    forest_reg = RandomForestRegressor(random_state=42)
    rnd_search = RandomizedSearchCV(forest_reg, param_distributions=param_distribs,
                                    n_iter=10, cv=5, scoring='neg_mean_squared_error', random_state=42)
    rnd_search.fit(housing_prepared, housing_labels)
    # 输出每一个树的得分与参数
    cvres = rnd_search.cv_results_
    for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
        print(np.sqrt(-mean_score), params)
    print("每个参数的重要性：")
    print("feature_importances:{}".format(grid_search.best_estimator_.feature_importances_))


if __name__ == "__main__":
    # main()
    # data_clean()
    housing_prepared, housing_labels = pipline()
    linear_model(housing_prepared, housing_labels)
    dtr(housing_prepared, housing_labels)