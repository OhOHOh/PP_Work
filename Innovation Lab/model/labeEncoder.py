import lightgbm as lgb
import pandas as pd
import numpy as np
import gc
import gzip
import os
from sklearn import preprocessing
from hdfs3 import HDFileSystem

hdfs = HDFileSystem(host='horton')


# 读取要用的Variable - 3001
path = '/vol/etl_jupyterdata1/home/runyu/public_notebooks/runyu/hdfs_data/smp_dataset/variable_3000.npy'
use_cols = list(np.load(path))  #list
#读取数据
path = "/user/runyu/data/masked/TSD/join_result_37_smp2_one_finalColType.csv"  #hdfs
with hdfs.open(path) as f:
    df = pd.read_csv(
        f, 
        low_memory=False, 
        na_values=['.', ' ', ''], 
        keep_default_na=False,
        skipinitialspace=True,
        memory_map=True
    )
    df = df[use_cols]  # 只采用3001维特征

# 对其中的object类型进行缺失值的填充! 统一填充为 MISSING123
object_variable_names = df.select_dtypes(include=['object']).columns
df[object_variable_names] = df[object_variable_names].fillna("MISSING123")
# 对其中的object类型进行 LabelEncoder !
le = preprocessing.LabelEncoder()
# score_dict = {}
for colNames in object_variable_names: #len(df.columns)
    le.fit(df.loc[:, colNames])
    df.loc[:, colNames] = le.transform(df.loc[:, colNames]) # 非常耗时
    # score_dict[colNames] = le.transform(df.loc[:, colNames])
    print("{:100} -done!".format(colNames))

# 对数据集进行保存
df.to_csv("/vol/etl_jupyterdata1/home/runyu/data/join_result_37_smp2_3000_object_labelEncoder.csv", index=False)
print("start upload to hdfs ...")
hdfs.put("/vol/etl_jupyterdata1/home/runyu/data/join_result_37_smp2_3000_object_labelEncoder.csv", 
         "/user/runyu/data/masked/TSD/join_result_37_smp2_3000_object_labelEncoder.csv")
print("start deleting local file ...")
cmd = "rm -f /vol/etl_jupyterdata1/home/runyu/data/join_result_37_smp2_3000_object_labelEncoder.csv"
os.system(cmd)
print("done!")
