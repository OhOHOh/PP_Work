import pandas as pd
import sys as sys
import os

df = pd.read_csv("./tripadv/home_page_info.csv")
# print(df['reviews'].sum())
# print(df.info('deep'))
# print(df.loc[2, 'name'])
print(df[df['reviews'] > 4000])

# df.loc[df['reviews'] > 4000, 'reviews'] = 4000
# print(df['reviews'].sum() * 0.8 / 600)

# s = "my name is runyu"
# print(sys.getsizeof(s))

# print(os.path.abspath(''))
# print(os.listdir(os.path.abspath('')))