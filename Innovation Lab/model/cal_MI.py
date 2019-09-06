import pandas as pd
import numpy as np
import gc
import gzip
from hdfs3 import HDFileSystem
hdfs = HDFileSystem(host='horton')

def entropy1(x): #用这个!
    # x is pd.Series, and already pd.cut
    counts = x.value_counts(normalize=True, dropna=False).values #ndarry
    return -counts.dot(np.log(counts+np.e**-100))

# 读取数据, 该数据集中所有的Variable都是Category类型的
path = "/user/runyu/data/masked/TSD/join_result_37_smp2_one_final_bins.csv"  #hdfs
with hdfs.open(path) as f:
    df = pd.read_csv(
        f, 
        low_memory=False, 
        na_values=['.', ' ', ''], 
        keep_default_na=False,
        skipinitialspace=True,
        memory_map=True
    )
    target = df['mm18_bad']  #已经修复了

rtn = pd.DataFrame()
rtn['name'] = df.columns

print("start cal own entropy ...")
# 计算自身的熵
for col_name in df.columns:
    rtn.loc[rtn['name']==col_name, 'own'] = entropy1(df[col_name])
    print("{:50} -own entropy done!".format(col_name))

# 计算与target的熵
print("start cal target entropy ...")
for col_name in df.columns:
    col_target_tmp = ["{}{}".format(i, j) for i,j in zip(df[col_name], target)]
    col_target = pd.Series(col_target_tmp)
    rtn.loc[rtn['name']==col_name, 'tmi'] = entropy1(col_target)
    print("{:50} -target entropy done!".format(col_name))

rtn.to_csv('./variable_target_mi.csv', index=False)