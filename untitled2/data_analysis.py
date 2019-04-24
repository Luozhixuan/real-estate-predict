#invite people for the Kaggle party
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
from scipy.stats import norm
from scipy import stats
from sklearn.preprocessing import StandardScaler
import warnings
import matplotlib.pyplot as plt
from pymongo import MongoClient
warnings.filterwarnings('ignore')


def load_data():
    try:
        client = MongoClient('localhost', 27017)  # connect db
        db = client['test']  # my db
        info = db['text_set']  # my collection
    except:
        print('connection error')

    data = pd.DataFrame(list(info.find()))  # find all data
    del data['_id']  # filter data
    dataset = data[['小区名称', '住房面积(平方米)', '平均价格(每平方)']]
    return dataset


def pandas_operations(dataset): # pandas基本操作
    dataset.info() #数据表基本信息
    dataset.dtypes #每一列的数据类型
    dataset.isnull() #拿到空值
    dataset['area'].unique() #看某一列的唯一值
    dataset.columns #查看列名称
    dataset.head() #前10行数据
    dataset.tail()
    dataset['column'].drop_duplicates() #删除重复值
    dataset['column'].replace('bj','test') #替换


def kaggle_party1(dataset): # 线图加直方图
    print(dataset['平均价格(每平方)'].describe())
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    sns.distplot(dataset['平均价格(每平方)']);
    plt.show()

def kaggle_party2(dataset):  # 散点状分布图
    var = '住房面积(平方米)'
    data = pd.concat([dataset['平均价格(每平方)'], dataset[var]], axis=1)
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    data.plot.scatter(x=var, y='平均价格(每平方)', ylim=(0, 800000));
    plt.show()

def kaggle_party3(dataset):
    k = 10  # number of variables for heatmap
    corrmat = dataset.corr()
    cols = corrmat.nlargest(k, '平均价格(每平方)')['平均价格(每平方)'].index
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    cm = np.corrcoef(dataset[cols].values.T)
    sns.set(font_scale=1.25)
    hm = sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f', annot_kws={'size': 10}, yticklabels=cols.values,
                     xticklabels=cols.values)
    plt.show()


def kaggle_party4(dataset): # check missing data and rates
    total = dataset.isnull().sum().sort_values(ascending=False)
    percent = (dataset.isnull().sum() / dataset.isnull().count().sort_values(ascending=False))
    missing_data = pd.concat([total, percent], axis=1, keys=['Total','Percent'])
    print(missing_data.head(20))
    # deal with missing data call drop


def kaggle_party5(dataset): #consider the range of price deviation
    saleprice_scaled = StandardScaler().fit_transform(dataset['平均价格(每平方)'][:, np.newaxis]);
    low_range = saleprice_scaled[saleprice_scaled[:, 0].argsort()][:10]
    high_range = saleprice_scaled[saleprice_scaled[:, 0].argsort()][-10:]
    print('outer range (low) of the distribution:')
    print(low_range)
    print('\nouter range (high) of the distribution:')
    print(high_range)

def kaggle_party6(dataset):
    # histogram and normal probability plot
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    sns.distplot(dataset['平均价格(每平方)'], fit=norm);
    fig = plt.figure()
    res = stats.probplot(dataset['平均价格(每平方)'], plot=plt)
    plt.show()


def kaggle_party7(dataset):
    # histogram and normal probability plot
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    dataset['平均价格(每平方)'] = np.log(dataset['平均价格(每平方)']) #log
    sns.distplot(dataset['平均价格(每平方)'], fit=norm);
    fig = plt.figure()
    res = stats.probplot(dataset['平均价格(每平方)'], plot=plt)
    plt.show()


def kaggle_party8(dataset):
    # using normality data
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    dataset['平均价格(每平方)'] = np.log(dataset['平均价格(每平方)']) #log
    plt.scatter(dataset['住房面积(平方米)'], dataset['平均价格(每平方)']);
    plt.show()


def drop_data(dataset):
    dataset = dataset.drop(dataset[dataset['平均价格(每平方)'] > 300000].index)
    dataset = dataset.drop(dataset[dataset['住房面积(平方米)'] > 600].index)
    return dataset


def main():
    dataset = load_data()
    dataset['住房面积(平方米)'] = pd.to_numeric(dataset['住房面积(平方米)'], errors='coerce')# convert str to int
    dataset['平均价格(每平方)'] = pd.to_numeric(dataset['平均价格(每平方)'], errors='coerce')# convert str to int
    # kaggle_party1(dataset)
    # kaggle_party2(dataset)
    # kaggle_party3(dataset)
    # kaggle_party4(dataset)
    # kaggle_party5(dataset)

    #data has been cleaned
    # dataset = drop_data(dataset)
    # kaggle_party2(dataset)
    # kaggle_party6(dataset)
    # kaggle_party7(dataset)
    kaggle_party8(dataset)


if __name__ == '__main__':
    main()