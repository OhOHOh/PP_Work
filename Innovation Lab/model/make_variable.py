import pandas as pd
import datetime
from IPython import display

# comments = pd.read_csv("../../../Innovation Lab/reviews_data_tripadv.csv")
# 'title', 'content','cabin', 'origin', 'destination', 'region', 'DOV', 'DOW', 'contribution', 'helpful', 'Tscore', 'LR', 'SC', 'FE', 'CS', 'VM', 'CL', 'CB', 'FB'
# groupby 每个公司,每个月的: 评论条数, 各个子项目评分的min,max,std,avg; 

# print(df.head(5))
def transform(dow):
    if len(dow) < 8 and dow != 'Today':
        dow = dow[:4] + '2019'
    return dow
def formDate(x):
    return datetime.datetime.strptime(x, '%b %Y').strftime('%Y-%m')
def make_variables(df):
    agg_func = {
        'cabin': ['nunique'],
        'LR': ['min', 'max', 'mean', 'std', 'median'], 
        'SC': ['min', 'max', 'mean', 'std', 'median'],
        'FE': ['min', 'max', 'mean', 'std', 'median'],
        'CS': ['min', 'max', 'mean', 'std', 'median'],
        'VM': ['min', 'max', 'mean', 'std', 'median'],
        'CL': ['min', 'max', 'mean', 'std', 'median'],
        'CB': ['min', 'max', 'mean', 'std', 'median'],
        'FB': ['min', 'max', 'mean', 'std', 'median'],
        'Tscore': ['min', 'max', 'mean', 'std', 'median'],
        'final_sen_score': ['min', 'max', 'mean', 'std', 'median', 'count'],
    }
    group = df.groupby(['companyName', 'DOW'])
    tmp = group.agg(agg_func)
    tmp.columns = ['_'.join(col).strip() for col in tmp.columns.values]
    tmp.reset_index(inplace=True)
    # 保存到本地
    tmp.sort_values(['companyName', 'DOW']).to_csv('../../../Innovation Lab/new_variables.csv', index=False)
    print(tmp.info())

def match_company(row_df, target_df):
    return 0

use_cols = ['companyName','cabin', 'region', 'DOV', 'DOW', 'contribution', 'helpful', 'Tscore', 'LR', 'SC', 'FE', 'CS', 'VM', 'CL', 'CB', 'FB', 'final_sen_score']
df = pd.read_csv("../../../Innovation Lab/reviews_data_tripadv_sen_score_change_sep.csv", sep='|', na_values=-1)
df = df[use_cols]
df = df.loc[df['DOW']!='Today']
df['DOW'] = df['DOW'].apply(transform)
df['DOW'] = df['DOW'].apply(formDate)
make_variables(df)
# read  result_with_tagging_name.csv
result_with_tagging_name = pd.read_csv(r'C:\Users\runyu\Documents\GithubWork\Innovation Lab\result_with_tagging_name.csv')
print(result_with_tagging_name.info())

