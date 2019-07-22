import pandas as pd
import sys as sys
import os

df = pd.read_csv("./tripadv/home_page_info.csv")
print(df['reviews'].sum())
print(df.info('deep'))
print(df.loc[2, 'name'])
for i in range(0, df.shape[0]):
    print(i)

# s = "my name is runyu"
# print(sys.getsizeof(s))

# print(os.path.abspath(''))
# print(os.listdir(os.path.abspath('')))