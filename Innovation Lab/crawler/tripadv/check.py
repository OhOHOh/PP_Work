import pandas as pd
import sys as sys
import os

df = pd.read_csv("./tripadv/home_page_info.csv")
print(df['reviews'].sum())
print(df.info('deep'))
print(df.loc[2, 'name'])
df.loc[df['reviews']>13000, 'reviews'] = 13000
print(
    df['reviews'].sum() * 0.8
)


# s = "my name is runyu"
# print(sys.getsizeof(s))

# print(os.path.abspath(''))
# print(os.listdir(os.path.abspath('')))