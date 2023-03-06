import pandas as pd
from . import clean
import pathlib
'''
code contributor: Miao Li
'''

def gen_data():
    '''
    calling all the clean function to generate data needed for visualization
    '''
    edu_data = pathlib.Path(__file__).parent / "../data/education.csv"
    fd_stamp = pathlib.Path(__file__).parent / "../data/food stamp.csv"
    income_data = pathlib.Path(__file__).parent /"../data/income.csv"
    pop_data = pathlib.Path(__file__).parent /"../data/population.csv"


    #demongraphic data
    df_edu = clean.clean_edu(edu_data)
    df_fdstamp = clean.clean_foodstamp(fd_stamp)
    df_inc = clean.clean_income(income_data)
    df_race = clean.clean_pop(pop_data)

    df_1 = pd.merge(df_edu, df_inc, on = 'NAME', how = 'left')

    df_2 = pd.merge(df_1, df_fdstamp, on = 'NAME', how = 'left')

    df_2.drop_duplicates(subset=['NAME'], keep='first', inplace=True, ignore_index=True)

    df_3 = pd.concat([df_2, df_race], axis = 1)
    
    df_3.to_csv("./cappyfoodies/cleaned_data/demo_data.csv")

    #restaurant data
    clean.clean_rest('./cappyfoodies/cleaned_data/business_cleaned.csv')

    print("data all cleaned!")