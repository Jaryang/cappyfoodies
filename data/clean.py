import pandas as pd
import re

def clean_edu(filename):
    '''
    take in the education data downloaded from census bureau and clean it
    '''
    edu_data = pd.read_csv(filename)

    df_edu = edu_data.filter(regex = "E$")
    df_edu = df_edu.drop([0])
    df_edu["NAME"] = df_edu['NAME'].str.extract(r'(\d{5})$')

    #calculate percentage of people with bachelor or higher degress
    df_edu = df_edu.rename(columns={'S1501_C01_006E': 'pop_over_25', 'S1501_C01_015E': '25_bach'})
    df_edu['per_bachelor'] = df_edu['25_bach'].astype(int)/df_edu['pop_over_25'].astype(int)
    df_edu.drop(df_edu.iloc[:, 1:-1], inplace=True, axis=1)

    return df_edu

def clean_foodstamp(filename):
    '''
    take in the food stamp data downloaded from census bureau and clean it
    '''
    fd_data = pd.read_csv(filename)

    df = fd_data[['NAME','S2201_C01_001E','S2201_C03_001E']]
    df = df.drop([0])
    df = df.rename(columns={'S2201_C01_001E': 'num_household', 'S2201_C03_001E': 'household_fd'})
    df["NAME"] = df['NAME'].str.extract(r'(\d{5})$')
    df['per_fdstamp'] = df['household_fd'].astype(int) / df['num_household'].astype(int)

    return df

def clean_income(filename):
    '''
    take in the income data downloaded from census bureau and clean it
    '''
    inc_data = pd.read_csv(filename)
    df = inc_data[inc_data['Label (Grouping)'].str.contains('household income')==True]
    df = df.filter(regex = '!Estimate')
    df.rename(columns = lambda x: x.replace('ZCTA5 ',"")[:5], inplace = True)
    df = df.T
    df['NAME'] =df.index
    df['med_hd_inc'] = df. iloc[:,0]
    df['mean_hd_inc'] = df. iloc[:,1]
    df.drop(df.iloc[:, 0:2], inplace=True, axis=1)

    return df

def clean_pop(filename):
    '''
    take in the income data downloaded from census bureau and clean it
    '''
    pop_data = pd.read_csv(filename)
    pop_data['Label (Grouping)'] = pop_data['Label (Grouping)'].str.strip()
    df = pop_data.filter(regex = '!Estimate')
    df.insert(0, 'Label', pop_data['Label (Grouping)'])
    df.rename(columns = lambda x: x.replace('ZCTA5 ',"")[:5], inplace = True)
    df_1 = df.drop([0,2,3,4,7,12])
    data = df_1.to_dict('series')

    for key, val in data.items():
        data[key] = data[key].tolist()

    return data
