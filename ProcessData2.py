import pandas as pd
import ast

def drop_duplicates(prod_list):
    another_list = []
    for item in prod_list:
        if item not in another_list:
            another_list.append(item)
    return another_list


df = pd.read_csv('process_data_2.csv')

df['prod_no'] = df['prod_no'].apply(ast.literal_eval)
df['prod_category'] = df['prod_category'].apply(ast.literal_eval)
#ChatGPT debug: https://chat.openai.com/share/b915e7a1-f3d1-44cc-90d4-83aa5f27cbe7

df['prod_no'] = df['prod_no'].apply(drop_duplicates)

exploded_df = df.apply(pd.Series.explode)
# https://pandas.pydata.org/docs/reference/api/pandas.Series.explode.html#pandas.Series.explode

df = exploded_df.drop(['prod_order_no'], axis=1)

df.to_csv('process_data_2.csv', index=False)