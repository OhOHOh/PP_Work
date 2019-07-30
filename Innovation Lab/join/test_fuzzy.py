from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd

a = "fuzzy"
listb = ['daghys', 'fuzzy', 'asdfag']
s = pd.Series(data=listb)
print(process.extractOne(a, s)[1]) # ('fuzzy', 100, 0)