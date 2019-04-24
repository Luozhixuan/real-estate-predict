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
from numpy import nan as NaN
from pymongo import MongoClient
warnings.filterwarnings('ignore')




#设置输出范围，防止输出省略
pd.set_option('display.max_columns',1000)
pd.set_option('display.max_rows', 3000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)

try:
    client = MongoClient('localhost', 27017)  # connect db
    db = client['test']  # my db
    info = db['wuhan_data']  # my collection
except:
    print('connection error')

data = pd.DataFrame(list(info.find()))  # find all data

del data['_id']  # filter data
dataset = data.loc[:,[ '所在区域', '平均价格(元/平方)', '房屋类型', '所在楼层', '建筑面积',
                        '建筑类型','房屋朝向','装修情况' ,'梯户比例' ,'配备电梯', '挂牌时间','上次交易时间','产权所属', '抵押信息']]

dataset['平均价格(元/平方)'] = pd.to_numeric(dataset['平均价格(元/平方)'], errors='coerce')# convert str to int
dataset= dataset[np.isnan(dataset['平均价格(元/平方)']) == False]#去空值 清洗数据

#区域
dataset['所在区域'][dataset['所在区域']=='洪山']=1
dataset['所在区域'][dataset['所在区域']=='江岸']=2
dataset['所在区域'][dataset['所在区域']=='东湖高新']=3
dataset['所在区域'][dataset['所在区域']=='武昌']=4
dataset['所在区域'][dataset['所在区域']=='黄陂']=5
dataset['所在区域'][dataset['所在区域']=='江夏']=6
dataset['所在区域'][dataset['所在区域']=='汉阳']=7
dataset['所在区域'][dataset['所在区域']=='硚口']=8
dataset['所在区域'][dataset['所在区域']=='东西湖']=9
dataset['所在区域'][dataset['所在区域']=='沌口开发区']=10
dataset['所在区域'][dataset['所在区域']=='青山']=11
dataset['所在区域'][dataset['所在区域']=='蔡甸']=12
dataset['所在区域'][dataset['所在区域']=='新洲']=13
dataset['所在区域'][dataset['所在区域']=='江汉']=14
dataset['所在区域'] = pd.to_numeric(dataset['所在区域'], errors='coerce')

#房屋类型？
str=dataset['房屋类型']
dataset['房屋类型']=dataset['房屋类型']


#所在楼层

#建筑类型？
dataset['建筑类型'][dataset['建筑类型']=='塔楼']=3
dataset['建筑类型'][dataset['建筑类型']=='板楼']=2
dataset['建筑类型'][dataset['建筑类型']=='板塔结合']=1
dataset['建筑类型'][dataset['建筑类型']=='暂无数据']=0

#装修情况
dataset['装修情况'][dataset['装修情况']=='精装']=1
dataset['装修情况'][dataset['装修情况']=='简装']=0.5
dataset['装修情况'][dataset['装修情况']=='毛坯']=0

#配备电梯
dataset['配备电梯'][dataset['配备电梯']=='有']=1
dataset['配备电梯'][dataset['配备电梯']=='无']=0.5
dataset['配备电梯'][dataset['配备电梯']=='暂无数据']=0

#产权所属
dataset['产权所属'][dataset['产权所属']=='共有']=1
dataset['产权所属'][dataset['产权所属']=='非共有']=0.5
dataset['产权所属'][dataset['产权所属']=='暂无数据']=0

#抵押信息

#dataset['抵押信息'][dataset['抵押信息']=='无抵押']
dataset['抵押信息'][dataset['抵押信息']=='暂无数据']=0
dataset.loc[:,('抵押信息')][dataset['抵押信息']=='无抵押']=1







#dataset['房屋类型'] = pd.to_numeric(dataset['房屋类型'], errors='coerce')

#print(np.isnan(dataset))
print(dataset)
print(dataset.describe())
dataset.to_csv("wuhan_train.csv",index=False,sep=',',encoding='utf_8_sig')
