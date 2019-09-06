import pandas as pd
import numpy as np
drop_cols = ['title', 'content']
df = pd.read_csv("../../../Innovation Lab/reviews_data_tripadv_sen_score_change_sep.csv", sep='|')
print(df.info())
print(df.head())