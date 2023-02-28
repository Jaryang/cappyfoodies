import csv
import pandas as pd
import clean

def gen_top_eth(filename):

    data = clean.clean_pop(filename)

    label = data['Label']

    for key, value in data.items():
        if key == 'Label':
            continue
        else:
            for i, val in enumerate(value):
                if i == 0:
                    pop_val = str(val).replace(',','')
                    total_pop = float(pop_val)
                value[i] = float(str(val).replace(',','')) / total_pop

    top_5 = {}
    
    for key, value in data.items():
        if key == 'Label':
            continue
        lst = sorted(range(len(value)), key=lambda i: value[i])[-6:]
        race_lst = []
        for x in lst[: : -1]:
            if x != 0:
                race = label[x]
                race_lst.append((race, value[x]))
        
        top_5[key] = race_lst

    with open('top_race.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        writer.writerow(['NAME', 'top_race'])
        for key, value in top_5.items():
            writer.writerow([key, value])

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

    #finalizing the final dataset
    # final = df_3.drop(df_3.columns[-2], axis = 1)
    print(df_3)


    # return df_3.drop(df_3.iloc[:,7], inplace = True)

    df_3.to_csv("demo_data.csv")

