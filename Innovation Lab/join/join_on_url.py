import pandas as pd
import os
import sys as sys
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def urlSplit_for_crawler(url):
    '''
    对字符串做一个分割, 指截取 www. .com 之间的
    '''
    if url == '.':
        return url
    url = url.replace('-', '')
    url = url.replace('*', '')
    url = url.replace(' ', '')
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
    try:
        str_list = url.split(".")
        if '/' in str_list[1]:
            tmp = str_list[0].split(":")
            return tmp[-1][2:]
        return str_list[1]
    except IndexError as e:
        # print(url)   # 大部分都是没有意义的
        pass


if __name__ == '__main__':
    # 读入爬虫的数据, 包含
    path = os.path.abspath(
        r'../crawler/tripadv/home_page_info.csv')  # print(path)
    crawler_df = pd.read_csv(path, usecols=['name', 'ComUrl'])
    crawler_df['MUrl'] = crawler_df['ComUrl'].apply(
        urlSplit_for_crawler)  # print(crawler_df.head(100))

    # 读入 PP 内部的数据, 用的是 Airlines_Travel sellers in Paypal.csv
    PP_df = pd.read_csv(
        r'C:\Users\runyu\Documents\Innovation Lab\Airlines_Travel sellers in Paypal.csv'
    )
    use_cols = ['busn_name', 'busn_supp_url', 'url']
    PP_df = PP_df[use_cols]
    PP_df['MurlPP'] = PP_df['url'].apply(urlSplit_for_PP)
    # print(PP_df['MurlPP'].head(100))

    # 比较 crawler_df['MUrl'] 中的 url 是否和 PP_df['MurlPP'] 中的 match 上
    '''
    count = 0
    for i in range(crawler_df.shape[0]):
        if crawler_df.loc[i, 'MUrl'] == '.':
            continue
        # if crawler_df.loc[i, 'MUrl'] in PP_df['MurlPP']:
        #     count += 1
        print(process.extractOne(crawler_df.loc[i, 'MUrl'], PP_df['MurlPP']))
    # print(count)
    '''
    print(process.extractOne(crawler_df.loc[0, 'MUrl'], PP_df['MurlPP']))
