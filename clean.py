import pandas as pd
import re
edu_data = pd.read_csv("education.csv")

df= edu_data.filter(regex = "E$")
df = df.drop([0])
df["NAME"] = df['NAME'].str.extract(r'(\d{5})$')
df.drop(df.iloc[:, 1:6], inplace=True, axis=1)
df.drop(df.iloc[:, 11:], inplace=True, axis=1)
df['per_bachelor'] = df['S1501_C01_015E'].astype(int)/df['S1501_C01_006E'].astype(int)
df.drop(df.iloc[:, 2:-2], inplace=True, axis=1)
df.to_csv("per_edu.csv",index = False)