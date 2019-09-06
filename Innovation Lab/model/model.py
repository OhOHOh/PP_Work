import lightgbm as lgb
import pandas as pd
import numpy as np
import gc
import gzip
import os
from sklearn.model_selection import KFold
from hdfs3 import HDFileSystem

hdfs = HDFileSystem(host='horton')

# 读取这3000列中哪些列是 object 的
object_variable_names_np = np.load("/vol/etl_jupyterdata1/home/runyu/public_notebooks/runyu/hdfs_data/smp_dataset/3000_object_variable.npy")
object_variable_names = list(object_variable_names_np)
#读取数据
path = "/user/runyu/data/masked/TSD/join_result_37_smp2_3000_object_labelEncoder.csv"  #hdfs
with hdfs.open(path) as f:
    df = pd.read_csv(
        f, 
        low_memory=False, 
        na_values=['.', ' ', ''], 
        keep_default_na=False,
        skipinitialspace=True,
        memory_map=True
    )
# 设置 train, target (model不用于预测, 所以使用全部数据)  
train = df.iloc[:, 1:]
target = df.iloc[:, 0]

# train model
# gbm = lgb.LGBMClassifier(
#     boosting_type='rf',
#     objective='multiclass',
#     num_class=3,
#     metric = 'multi_error',
#     learning_rate = 0.01,
#     num_leaves = 35,
#     feature_fraction=0.8,
#     bagging_fraction=0.6,
#     bagging_freq= 8,
#     lambda_l1= 0.6,
#     lambda_l2= 0,
#     verbose = -1,
# )
param = {
    'boosting': 'rf', 
    'objective': 'multiclass',
    'num_class': 3, 
    'metric': 'multi_error',
    'max_depth': -1,
    'min_data_in_leaf': 20,
    'learning_rate': 0.01,
    max_bin=511,
    subsample=0.9,         #表示训练样本的采样比例
    subsample_freq=5,      #每3次，才进行行采样
    colsample_bytree=0.8,  #样本采样频率
    'feature_fraction': 0.8,    #特征筛选
    'feature_fraction_seed': 2,
    'min_data_in_bin': 3
}
# k-折交叉验证
folds = KFold(n_splits=5, shuffle=True, random_state=2019)
oof = np.zeros(len(train))

feature_importance_df = pd.DataFrame()
for fold_, (trn_idx, val_idx) in enumerate(folds.split(train.values, target.values)): # train->X, target->y
    print("fold n°{}".format(fold_))
    trn_data = lgb.Dataset(train.iloc[trn_idx, :],
                           label=target.iloc[trn_idx],
                           categorical_feature=object_variable_names
                          )
    val_data = lgb.Dataset(train.iloc[val_idx, :],
                           label=target.iloc[val_idx],
                           categorical_feature=object_variable_names
                          )
    num_round = 10000
    clf = lgb.train(param,
                    train_set=trn_data,
                    num_boost_round=num_round,
                    valid_sets = [trn_data, val_data],
                    verbose_eval=100, #每隔verbose_eval 个 boosting stage 打印对验证集评估的metric
                    early_stopping_rounds = 200)
    
    oof[val_idx] = clf.predict(train.iloc[val_idx][features], num_iteration=clf.best_iteration)
    
    fold_importance_df = pd.DataFrame()
    fold_importance_df["feature"] = train.columns
    fold_importance_df["importance"] = clf.feature_importance()
    fold_importance_df["fold"] = fold_ + 1
    feature_importance_df = pd.concat([feature_importance_df, fold_importance_df], axis=0)
    





