import pandas as pd
import os
import sys as sys
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

if __name__ == '__main__':
    # 读取爬虫爬取的数据
    path = os.path.abspath(
        r'../crawler/tripadv/home_page_info.csv')  # print(path)
    crawler_df = pd.read_csv(path, usecols=['name', 'ComUrl'])

    # 读取 PP 内部的数据
    use_cols_for_PP = ['busn_name', 'busn_supp_url', 'url']
    PP_df = pd.read_csv(
        r'C:\Users\runyu\Documents\Innovation Lab\Airlines_Travel sellers in Paypal.csv',
        usecols=use_cols_for_PP)

    # 开始查找 1. 不做任何修改直接查找
    count = 0
    for i in range(crawler_df.shape[0]):
        if crawler_df.loc[i, 'name'] == '.':
            continue
        if crawler_df.loc[i, 'name'] in PP_df['busn_name']:
            count = count + 1
        print(process.extractOne(crawler_df.loc[i, 'name'],
                                 PP_df['busn_name']))
    print(count)
