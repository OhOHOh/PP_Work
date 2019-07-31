import pandas as pd
import numpy as np
import os
import time
import sys as sys
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from contextlib import contextmanager


@contextmanager
def timer(name):
    t0 = time.time()
    yield
    print("{} -done in {:.0f}s".format(name, time.time() - t0))


def matcher1(crawler_df, PP_df, join_result):
    '''
    不做任何预处理, 直接比较 name, busn_name
    '''
    count = 0
    for i in range(crawler_df.shape[0]):
        if crawler_df.loc[i, 'name'] == '.':
            continue
        rtn = process.extractOne(crawler_df.loc[i, 'name'], PP_df['busn_name'])
        print(rtn)
        if rtn[1] == 100:  # 完全match
            join_result.loc[join_result['nameC'] == crawler_df.loc[i, 'name'],
                            'cust_idPP'] = PP_df.loc[rtn[2], 'cust_id']
            count = count + 1
    print("totally(100%) match: {}".format(count))


def matcher2(crawler_df, PP_df, join_result):
    '''
    将2个 df 中的 name, busn_name 小写
    然后使用 process.extractOne(a, b, scorer=fuzz.token_sort_ratio) 来不按顺序地 match
    But: matcher1 中已经 100分的pair不参与 matcher2 中
    '''
    crawler_df['name'] = crawler_df['name'].str.lower()
    PP_df['busn_name'] = PP_df['busn_name'].str.lower()
    count = 0
    for i in range(crawler_df.shape[0]):
        if ~np.isnan(join_result.loc[i, 'cust_idPP']) or crawler_df.loc[i, 'name'] == '.':
            continue
        rtn = process.extractOne(crawler_df.loc[i, 'name'],
                                 PP_df['busn_name'],
                                 scorer=fuzz.token_sort_ratio)
        print(rtn)
        if rtn[1] == 100 and PP_df.loc[rtn[2], 'cust_id'] not in join_result['cust_idPP'].values:
            join_result.loc[join_result['nameC'] == crawler_df.loc[i, 'name'], 'cust_idPP'] = PP_df.loc[rtn[2], 'cust_id']
            count = count + 1
    print("totally(100%) match: {}".format(count))


if __name__ == '__main__':
    join_result = pd.DataFrame(columns=['nameC', 'cust_idPP'])
    # 1.读取爬虫爬取的数据
    path = os.path.abspath(
        r'../crawler/tripadv/home_page_info.csv')  # print(path)
    crawler_df = pd.read_csv(path, usecols=['name', 'ComUrl'])
    # 填充 join_result['nameC']
    join_result['nameC'] = crawler_df['name']
    join_result['cust_idPP'] = np.nan

    # 2.读取 PP 内部的数据
    use_cols_for_PP = ['cust_id', 'busn_name', 'busn_supp_url', 'url']
    PP_df = pd.read_csv(
        "../../../Innovation Lab/Airlines_Travel sellers in Paypal.csv",
        usecols=use_cols_for_PP)

    # 3.开始-Match 1. 不做任何修改直接查找 - 116
    # with timer("1 - No Modify"):
    #     matcher1(crawler_df, PP_df, join_result)
    # join_result.to_csv("./result2.csv")

    # 4.开始-Match 2. 去除mtach1中完全匹配到的, 再将所有字母小写, 使用不按顺序的规则
    join_result = pd.read_csv("./result2.csv")
    with timer("2 - lower and scorer=fuzz.token_sort_ratio"):
        matcher2(crawler_df, PP_df, join_result)
