import pandas as pd


df = pd.read_csv('/temp/LEC_01_data.csv')
print(df)

df_name_age = df[['Name','Age']]
print(df_name_age)