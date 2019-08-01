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


def urlSplit_for_crawler(url):
    '''
    对字符串做一个分割, 指截取 www. .com 之间的
    '''
    if url == '.':
        return url
    url = url.replace('-', '')
    url = url.replace('*', '')
    url = url.replace(' ', '')
    url = url.lower()
    str_list = url.split(".")
    if '/' in str_list[1]:
        tmp = str_list[0].split(":")
        return tmp[-1][2:]
    return str_list[1]


def urlSplit_for_PP(url):
    '''
    对字符串做一个分割, 指截取 www. .com 之间的
    '''
    del_list = [
        '#', 'http://', 'http:/', 'http:', 'http://-', 'none', 'www.ebay.co.uk'
    ]
    if url in del_list:
        return url

    url = str(url) + '/'
    url = url.replace('-', '')
    url = url.replace('*', '')
    url = url.replace(' ', '')
    url = url.lower()
    try:
        str_list = url.split(".")
        if '/' in str_list[1]:
            tmp = str_list[0].split(":")
            return tmp[-1][2:]
        return str_list[1]
    except IndexError as e:
        # print(url)   # 大部分都是没有意义的
        pass


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
        if ~np.isnan(join_result.loc[i, 'cust_idPP']
                     ) or crawler_df.loc[i, 'name'] == '.':
            continue
        rtn = process.extractOne(crawler_df.loc[i, 'name'],
                                 PP_df['busn_name'],
                                 scorer=fuzz.token_sort_ratio)
        print(rtn)
        if rtn[1] == 100 and PP_df.loc[rtn[2], 'cust_id'] not in join_result[
                'cust_idPP'].values:
            join_result.loc[join_result['nameC'] == crawler_df.loc[i, 'name'],
                            'cust_idPP'] = PP_df.loc[rtn[2], 'cust_id']
            count = count + 1
    print("totally(100%) match: {}".format(count))


def matcher3(crawler_df, PP_df, join_result):
    '''
    直接对 url 进行匹配
    '''
    crawler_df['ComUrl'] = crawler_df['ComUrl'].apply(urlSplit_for_crawler)
    PP_df['url'] = PP_df['url'].apply(urlSplit_for_PP)
    count = 0
    for i in range(crawler_df.shape[0]):
        if ~np.isnan(join_result.loc[i, 'cust_idPP']) or crawler_df.loc[i, 'ComUrl'] == '.':  # 去除crwaler_df中已经匹配到的
            continue
        # for j in range(PP_df.shape[0]):
        #     if PP_df.loc[j, 'cust_id'] in join_result['cust_idPP'].values or np.isnan(PP_df.loc[j, 'url']):  # 去除PP_df中匹配到的
        #         continue
        #     if crawler_df.loc[i, 'ComUrl'] in PP_df.loc[j, 'url']:
        #         join_result.loc[join_result['nameC'] ==crawler_df.loc[i, 'name'],'cust_idPP'] = PP_df.loc[j, 'cust_id']
        #         count = count + 1

        if PP_df['url'].str.contains(crawler_df.loc[i, 'ComUrl']).any():
            df = PP_df[PP_df['url'].str.contains(crawler_df.loc[i, 'ComUrl'], na=False)]
            rtn = process.extractOne(crawler_df.loc[i, 'ComUrl'], df['url'])
            print(rtn)
            join_result.loc[join_result['nameC'] == crawler_df.loc[i, 'name'],'cust_idPP'] = df.loc[rtn[2], 'cust_id']
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

    # 3.开始-Match 1. 不做任何修改直接查找 - 116个 10000+s
    # with timer("1 - No Modify"):
    #     matcher1(crawler_df, PP_df, join_result)
    # join_result.to_csv("./result2.csv")

    # 4.开始-Match 2. 去除mtach1中完全匹配到的, 再将所有字母小写, 使用不按顺序的规则 - 2个 1810s
    # join_result = pd.read_csv("./result1.csv")
    # with timer("2 - lower and scorer=fuzz.token_sort_ratio"):
    #     matcher2(crawler_df, PP_df, join_result)
    # join_result.to_csv("./result2.csv")

    # 5.开始- Match 3. 用上url - match 189
    join_result = pd.read_csv("./result2.csv")
    with timer("3 - lower based on url"):
        matcher3(crawler_df, PP_df, join_result)
    join_result.to_csv("./result3.csv")
