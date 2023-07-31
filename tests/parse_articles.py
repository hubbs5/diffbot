import os
import sys
import json
import pandas as pd

try:
    from ..diffbot.knowledge_graph import article
except:
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from diffbot.knowledge_graph import article


data = json.load(open("diffbot.json", "r"))

df = pd.DataFrame.from_dict(article.parse_articles(data), orient="index").reset_index()
print(df.shape)
print(df.columns)
df.to_csv('diffbot.csv')