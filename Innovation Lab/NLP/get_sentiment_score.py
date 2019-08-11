import pandas as pd
import numpy as np
from textblob import TextBlob

comments = pd.read_csv("../../../Innovation Lab/reviews_data_tripadv.csv")
print(comments.columns)
# textblob = TextBlob(comments.loc[0, 'content'])
# print(textblob.sentiment.polarity)
# textblob = TextBlob(comments.loc[0, 'title'])
# print(textblob.sentiment.polarity)

# 计算2个 sentiment score: tilte & content
comments['title_sen_score'] = np.nan
comments['content_sen_score'] = np.nan
comments['final_sen_score'] = np.nan

for i in range(comments.shape[0]):
    try:
        comments.loc[i, 'title_sen_score'] = TextBlob(comments.loc[i, 'title']).sentiment.polarity
    except Exception as e:
        print("title error: ".format(e))
    try:
        comments.loc[i, 'content_sen_score'] = TextBlob(comments.loc[i, 'content']).sentiment.polarity
    except Exception as e:
        print("contnet error: ".format(e))
    try:
        comments.loc[i, 'final_sen_score'] = 0.4*comments.loc[i, 'title_sen_score'] + 0.6*comments.loc[i, 'content_sen_score']
    except Exception as e:
        print("final error: {}".format(e))
    print("{:10} comments finished!".format(i))


comments.to_csv("../../../Innovation Lab/reviews_data_tripadv_sen_score_change_sep.csv", index=False, sep='|')
