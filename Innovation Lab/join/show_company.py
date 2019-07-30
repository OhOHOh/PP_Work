import pandas as pd
import os
import sys as sys


def urlSplit(url):
    '''
    对字符串做一个分割, 指截取 www. .com 之间的
    例子: https://www.adria.si/en/, https://air-swift.com/ 
    http://africanexpress.net/
    https://airalgerie.dz/
    '''
    url = url.replace('-', '')
    str_list = url.split(".")
    if '/' in str_list[1]:
        tmp = str_list[0].split(":")
        return tmp[-1][2:]
    return str_list[1]


# 获取当前目录和文件: https://www.cnblogs.com/Jomini/p/8636129.html
# print(os.path.abspath('.'))
# print(os.listdir(os.path.abspath('')))

path = os.path.abspath(r'../crawler/tripadv/home_page_info.csv')  # print(path)
df = pd.read_csv(path, usecols=['name', 'ComUrl'])
df['MUrl'] = df['ComUrl'].apply(urlSplit)
print(df.head(100))
