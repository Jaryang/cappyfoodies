import csv
import pandas as pd
import clean

def gen_data():

    df_edu = clean.clean_edu("education.csv")
    print(type(df_edu['NAME']))
    df_fdstamp = clean.clean_foodstamp("food stamp.csv")
    df_inc = clean.clean_income("income.csv")

    gen_top_eth("population.csv")

    df_race = pd.read_csv('top_race.csv')
    df_race["NAME"].astype(str)
    print(type(df_race['NAME']))

    df_1 = pd.merge(df_edu, df_inc, on = 'NAME', how = 'left')

    df_2 = pd.merge(df_1, df_fdstamp, on = 'NAME', how = 'left')

    df_2.drop_duplicates(subset=['NAME'], keep='first', inplace=True, ignore_index=True)

    df_3 = pd.concat([df_2, df_race], axis = 1)
    
    df_3.to_csv("demo_data.csv")

