# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


info = pd.read_csv('meal_order_info.csv', encoding='utf-8')
info_before = pd.read_csv('info_new.csv', encoding='utf-8')

# 将两个数据拼起来
info_all = pd.concat([info_before, info])
print('查看各表的维数：\n', info.shape, info_before.shape, info_all.shape)
info.head()
# 条件选取order_status==1的数据
info = info_all[info_all['order_status'].isin(['1'])]
info = info.reset_index(drop=True)
for i,k in enumerate(info['use_start_time']):
    y=k.split()
    y=pd.to_datetime(y[0])
    info.loc[i,'use_start_time']=y

groupbyday= info[['use_start_time','number_consumers','accounts_payable']].groupby(by='use_start_time')
sale_day=groupbyday.sum()
sale_day.columns=['人数','销量']
print(sale_day)
# 每日用餐人数折线图
# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(12, 6))
plt.title('每日用餐人数折线图')
plt.xlabel('日期')
plt.ylabel('用餐人数')
plt.plot(sale_day['人数'])
plt.show()

# 画出每日销售额的折线图
# 新建画板
plt.figure(figsize=(12, 6))
plt.title('每日销售额的折线图')
plt.xlabel('日期')
plt.ylabel('销售额')
plt.plot(sale_day['销量'])
plt.show()


info_august = pd.read_csv('meal_order_info.csv', encoding='utf-8')
users_august = pd.read_csv('users.csv', encoding='utf-8')

# 提取订单状态为1的数据
info_august_new = info_august[info_august['order_status'].isin(['1'])]
info_august_new = info_august_new.reset_index(drop=True)
print('提取的订单数据维数：', info_august_new.shape)

print(info_august_new.head())
info_august_new.to_csv('info_august_new.csv', index=False, encoding='utf-8')

# 匹配用户的最后一次用餐时间
for i in range(1, len(info_august_new)):
    num = users_august[users_august['USER_ID'] ==
                       info_august_new.iloc[i - 1, 1]].index.tolist()
    users_august.iloc[num[0], 14] = info_august_new.iloc[i - 1, 9]
    users_august.iloc[num[0], 14] = info_august_new.iloc[i - 1, 9]

user = users_august
user['LAST_VISITS'] = user['LAST_VISITS'].fillna(999)
user = user.drop(user[user['LAST_VISITS'] == 999].index.tolist())
user = user.iloc[:, [0, 2, 12, 14]]
user.head()

# 读取数据
users = pd.read_csv('user_loss.csv', encoding='gbk')
info = pd.read_csv('info_new.csv', encoding='utf-8')
print('历史客户信息表的维数：', users.shape)
print('历史订单表的维数：', info.shape)

# 将时间转为时间格式
users['CREATED'] = pd.to_datetime(users['CREATED'])
info['use_start_time'] = pd.to_datetime(info['use_start_time'])
info['lock_time'] = pd.to_datetime(info['lock_time'])

# 匹配用户的最后一次用餐时间
for i in range(len(users)):
    info1 = info.iloc[info[info['name'] == users.iloc[i, 2]].index.tolist(), :]
    if sum(info['name'] == users.iloc[i, 2]) != 0:
        users.iloc[i, 14] = max(info1['use_start_time'])

# 特征选取
# 提取有效订单
info = info.loc[info['order_status'] == 1, ['emp_id', 'number_consumers', 'expenditure']]
info = info.rename(columns={'emp_id': 'USER_ID'})  # 修改列名
info.head()

info_user.to_csv('info_user.csv', index=False, encoding='utf-8')

import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np

user_value1.columns = ['USER_ID', 'F']  # 修改列名
print('F特征的最大值：', max(user_value1['F']))
print('F特征的最小值：', min(user_value1['F']))

# 构建M特征
user_value2 = info[['emp_id', 'expenditure']].groupby(by='emp_id').sum()
user_value2 = pd.DataFrame(user_value2).reset_index()
user_value2.columns = ["USER_ID", "M"]
user_value = pd.merge(user_value1, user_value2, on='USER_ID')
print('M特征的最大值：', max(user_value['M']))
print('M特征的最小值：', min(user_value['M']))

# 构建R特征
user_value = pd.merge(user_value, user, on='USER_ID')  # 合并两个表
# 转换时间格式
for i, k in enumerate(user_value['LAST_VISITS']):
    y = k.split()
    y = pd.to_datetime(y[0])
    user_value.loc[i, 'LAST_VISITS'] = y
last_time = pd.to_datetime(user_value['LAST_VISITS'])
deadline = pd.to_datetime("2016-8-31")  # 观测窗口结束时间
user_value['R'] = deadline - last_time
print('R特征的最大值：', max(user_value['R']))
print('R特征的最小值：', min(user_value['R']))

# 代码 7-5
# 特征提取
user_value = user_value.iloc[:, [0, 3, 6, 1, 2]]
user_value.to_csv("user_value.csv", encoding="utf-8_sig", index=False)

USER_ID = user_value['USER_ID']
ACCOUNT = user_value['ACCOUNT']
user_value = user_value.iloc[:, [2, 3, 4]]
user_value.iloc[:, 0] = [i.days for i in user_value.iloc[:, 0]]

# 标准差标准化
standard = StandardScaler().fit_transform(user_value)
np.savez('standard.npz', standard)
print(standard)

standard = np.load('standard.npz')['arr_0']
k = 3  # 聚类中心数

# 构建模型
kmeans_model = KMeans(n_clusters=k, n_jobs=3, random_state=123)
fit_kmeans = kmeans_model.fit(standard)  # 模型训练
print('聚类中心：\n', kmeans_model.cluster_centers_)

print('样本的类别标签：\n', kmeans_model.labels_)

# 统计不同类别样本的数目
r1 = pd.Series(kmeans_model.labels_).value_counts()
print('最终每个类别的数目为：\n', r1)

# 代码 7-7
# %matplotlib inline
import matplotlib.pyplot as plt

# 中文和负号的正常显示
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

# 绘制雷达图
N = len(kmeans_model.cluster_centers_[0])
# 设置雷达图的角度，用于平分切开一个圆面
angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
# 为了使雷达图一圈封闭起来
angles = np.concatenate((angles, [angles[0]]))

# 绘图
fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, polar=True)
sam = ['r', 'g', 'b']
lstype = ['-', '--', '-.']
lab = []
for i in range(len(kmeans_model.cluster_centers_)):
    values = kmeans_model.cluster_centers_[i]
    feature = ['R', 'F', 'M']
    values = np.concatenate((values, [values[0]]))
    # 绘制折线图
    ax.plot(angles, values, sam[i], linestyle=lstype[i], linewidth=2, markersize=10)
    ax.fill(angles, values, alpha=0.5)  # 填充颜色
    # ax.set_thetagrids(angles * 180 / np.pi, feature, fontsize=15)  # 添加每个特征的标签
    plt.title('客户群特征分布图')  # 添加标题
    ax.grid(True)
    lab.append('客户群' + str(i + 1))
plt.legend(lab)
# plt.savefig('征分布图.png')
plt.show()
plt.close
