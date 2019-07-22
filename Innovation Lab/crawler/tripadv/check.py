import pandas as pd
import sys as sys

df = pd.read_csv("./home_page_info.csv")
# print(df['reviews'].sum())
# print(df.info('deep'))

s = "my name is runyu"
print(sys.getsizeof(s))
