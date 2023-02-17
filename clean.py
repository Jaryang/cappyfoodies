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
    df_edu.drop(df_edu.iloc[:, 1:6], inplace=True, axis=1)
    df_edu.drop(df_edu.iloc[:, 11:], inplace=True, axis=1)
    df_edu['per_bachelor'] = df_edu['S1501_C01_015E'].astype(int)/df['S1501_C01_006E'].astype(int)
    df_edu.drop(df.iloc[:, 2:-2], inplace=True, axis=1)

    return df_edu

def clean_foodstamp(filename):
    '''
    take in the food stamp data downloaded from census bureau and clean it
    '''
    fd_data = pd.read_csv(filename)

    df = fd_data[['NAME','S2201_C01_001E','S2201_C03_001E']]
    df = df.drop([0])
    df["NAME"] = df['NAME'].str.extract(r'(\d{5})$')
    df['per_fdstamp'] = df['S2201_C03_001E'].astype(int) / df['S2201_C01_001E'].astype(int)
    
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
    
    return df

def clean_pop(filename):
    '''
    take in the income data downloaded from census bureau and clean it
    '''
    pop_data = pd.read_csv("population.csv")
    pop_data['Label (Grouping)'] = pop_data['Label (Grouping)'].str.strip()
    df = pop_data.filter(regex = '!Estimate')
    df.insert(0, 'Label', pop_data['Label (Grouping)'])
    df.rename(columns = lambda x: x.replace('ZCTA5 ',"")[:5], inplace = True)
    df_1 = df.drop([0,2,3,4,7,12])
    df_2 = df_1.T
    df.to_dict('series')

    for key, val in data.items():
        data[key] = data[key].tolist()

    return data

def gen_top_eth(filename):

    data = clean_pop(filename)

    label = data['Label']

    for key, value in data.items():
        if key == 'Label':
            continue
        else:
            for i, val in enumerate(value):
                if i == 0:
                    total_pop = float(val.replace(',',''))
                value[i] = float(val.replace(',','')) / total_pop

    top_5 = {}
    for key, value in data.items():
        if key == 'Label':
            continue
        lst = sorted(range(len(value)), key=lambda i: value[i])[-5:]
        race_lst = []
        for x in lst[: : -1]:
            if x != 0:
                race = label[x]
                race_lst.append((race, value[x]))
        top_5[key] = race_lst

    with open('top_race.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in top_5.items():
       writer.writerow([key, value])





