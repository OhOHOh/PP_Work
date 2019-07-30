import pandas as pd


# df = pd.read_csv(r'C:\Users\runyu\Documents\Innovation Lab\SQLAExport.txt', sep='\t')
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


df = pd.read_csv(
    r'C:\Users\runyu\Documents\Innovation Lab\Airlines_Travel sellers in Paypal.csv'
)
use_cols = ['busn_name', 'busn_supp_url', 'url']
df = df[use_cols]
# print(df.url.value_counts())
df['MurlPP'] = df['url'].apply(urlSplit_for_PP)
print(df['MurlPP'].head(100))
