import pandas as pd
import datetime

strn = "11.1"
# print(strn.isdigit())
# print(strn.isnumeric())
# print(strn.isalnum())

# strn = 'Jul 4'
# strn = strn[:4] + '2019'
# print(strn)

# detester = '2017-01-01'
detester = 'Jul 2019'
date = datetime.datetime.strptime(detester, '%M %Y')
print(date)
