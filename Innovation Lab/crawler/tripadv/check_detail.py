import pandas as pd
import os


def get_files(path):
    files_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            files_list.append(os.path.join(root, file))
    return files_list

if __name__ == '__main__':
    path = r'C:/Users/Runshen/Desktop/detail_page_reviews_per_company/'
    files_list = get_files(path=path)
    # count = 0
    use_cols = ['companyName', 'title', 'content', 'cabin', 'origin',
       'destination', 'region', 'DOV', 'DOW', 'contribution', 'helpful',
       'Tscore', 'LR', 'SC', 'FE', 'CS', 'VM', 'CL', 'CB', 'FB']
    rtn_df = pd.DataFrame(columns=use_cols)
    for file in files_list:
        df = pd.read_csv(file, usecols=use_cols)
        # count += df.shape[0]
        rtn_df = pd.concat(objs=[rtn_df, df], ignore_index=True)
    # print(count)
    rtn_df.to_csv(r'C:/Users/Runshen/Desktop/detail_page_reviews_per_company/summary.csv', index=False)

    # df = pd.read_csv(files_list[0])
    # print(df.columns)
