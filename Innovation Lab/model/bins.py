import pandas as pd
import numpy as np
import gc
import gzip
import os
from hdfs3 import HDFileSystem

hdfs = HDFileSystem(host='horton')

# 读入新的10W的数据集
path = "/user/runyu/data/masked/TSD/join_result_37_smp2_one_finalColType.csv"
with hdfs.open(path) as f:
    df = pd.read_csv(
        f, 
        low_memory=False, 
        na_values=['.', ' ', ''], 
        keep_default_na=False,
        skipinitialspace=True,
        memory_map=True, # map the file object directly onto memory and access the data directly from there. Using this option can improve performance because there is no longer any I/O overhead.
    )                                                                                                                                                                                                                           
    print(df.info())

# final_float_variable_names
final_number_variable_names = df.select_dtypes(include=['float', 'int']).columns # print(final_float_variable_names)
for variable_name in final_number_variable_names:
    # 分箱
    df[variable_name] = pd.cut(df[variable_name], 10, labels=[0,1,2,3,4,5,6,7,8,9])
    print("{:50} -done!".format(variable_name))

    
# 保存 - 还未运行 - 是由缺陷的！gloss和mm18_bad也被cut了！明天修改！
print("start saving result to local ...")
df.to_csv("/vol/etl_jupyterdata1/home/runyu/data/join_result_37_smp2_one_final_bins.csv", index=False)
print("start upload to hdfs ...")
hdfs.put("/vol/etl_jupyterdata1/home/runyu/data/join_result_37_smp2_one_final_bins.csv", 
         "/user/runyu/data/masked/TSD/join_result_37_smp2_one_final_bins.csv")
print("start deleting local file ...")
cmd = "rm -f /vol/etl_jupyterdata1/home/runyu/data/join_result_37_smp2_one_final_bins.csv"
os.system(cmd)
print("done!")
