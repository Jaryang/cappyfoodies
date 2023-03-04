import pandas as pd
import clean_func.clean

def gen_data():
    '''
    calling all the clean function to generate data needed for visualization
    '''

    #demongraphic data
    df_edu = clean.clean_edu("../data/education.csv")
    df_fdstamp = clean.clean_foodstamp("../data/food stamp.csv")
    df_inc = clean.clean_income("../data/income.csv")
    df_race = clean.clean_pop('../data/population.csv')

    df_1 = pd.merge(df_edu, df_inc, on = 'NAME', how = 'left')

    df_2 = pd.merge(df_1, df_fdstamp, on = 'NAME', how = 'left')

    df_2.drop_duplicates(subset=['NAME'], keep='first', inplace=True, ignore_index=True)

    df_3 = pd.concat([df_2, df_race], axis = 1)
    
    df_3.to_csv("../cleaned_data/demo_data.csv")

    #restaurant data
    clean.clean_rest('../data/business_cleaned_v3.csv')