import pandas as pd
from textblob import TextBlob

wiki = TextBlob("Textblob is amazingly simple to use. What great fun!")

print(wiki.sentiment)

