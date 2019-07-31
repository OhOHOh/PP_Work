from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
import numpy as np

a = "fu zzy"
listb = ['dag hys', 'fu zzy', 'asdf ag', 'zzy fu']
s = pd.Series(data=listb)
print(s.str.upper())
# print(process.extractOne(a, s))  # ('fuzzy', 100, 0)
# print(process.extractOne(a, s, scorer=fuzz.token_sort_ratio))
# print(a not in s.values)

# df = pd.read_csv("./result2.csv")
# print(np.isnan(df.loc[0, 'cust_idPP']))
# print(np.isnan(df.loc[1, 'cust_idPP']))