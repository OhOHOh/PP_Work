import pandas as pd
import datetime

df = None

print(df is not None)


runyu = datetime.datetime.now() - datetime.timedelta(days=1)
print(runyu.year)
print(runyu.day)
print(runyu.strftime("%b %d"))
