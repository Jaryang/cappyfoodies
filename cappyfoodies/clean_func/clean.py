import pandas as pd
import re
import csv
from .category_dict import cate_dct, Not_Food, Sub_Category
'''
Code contributor: Miao Li
'''

def clean_edu(filename):
    '''
    take in the education data downloaded from census bureau and clean it
    Input:
        filename (string)
    
    Output:
        df_edu (pandas dataframe)
    '''
    edu_data = pd.read_csv(filename)

    #getting zipcode and the estimated number 
    df_edu = edu_data.filter(regex = "E$")
    df_edu["NAME"] = df_edu['NAME'].str.extract(r'(\d{5})$')
    df_edu = df_edu.drop([0])

    #calculate percentage of people with bachelor or higher degress among population over 25
    df_edu = df_edu.rename(columns={'S1501_C01_006E': 'pop_over_25', 'S1501_C01_015E': '25_bach'})
    df_edu['per_bachelor'] = df_edu['25_bach'].astype(int)/df_edu['pop_over_25'].astype(int)
    df_edu.drop(df_edu.iloc[:, 1:-1], inplace=True, axis=1)

    return df_edu

def clean_foodstamp(filename):
    '''
    take in the food stamp data downloaded from census bureau and clean it
    Input:
        filename (string)
    
    Output:
        df (pandas dataframe)
    '''
    fd_data = pd.read_csv(filename)

    df = fd_data[['NAME','S2201_C01_001E','S2201_C03_001E']]
    df = df.drop([0]) #drop the non-numeric row
    df = df.rename(columns={'S2201_C01_001E': 'num_household', 'S2201_C03_001E': 'household_fd'})
    df["NAME"] = df['NAME'].str.extract(r'(\d{5})$')

    #calculate the percentage of household eligible for food stamp
    df['per_fdstamp'] = df['household_fd'].astype(int) / df['num_household'].astype(int)

    return df


def clean_income(filename):
    '''
    take in the income data downloaded from census bureau and clean it
    Input:
        filename (string)
    
    Output:
        df (pandas dataframe)
    '''
    inc_data = pd.read_csv(filename)

    #filter the estimate of household income
    df = inc_data[inc_data['Label (Grouping)'].str.contains('household income')==True]
    df = df.filter(regex = '!Estimate')

    #change the name to zipcode and transpose
    df.rename(columns = lambda x: x.replace('ZCTA5 ',"")[:5], inplace = True)
    df = df.T
    df['NAME'] =df.index
    df['med_hd_inc'] = df.iloc[:,0]
    df['mean_hd_inc'] = df.iloc[:,1]
    df.drop(df.iloc[:, 0:2], inplace=True, axis=1)

    return df

def find_top_race(data, top_num):
    '''
    Finding the most frequent categories in a dataset, return a 
        dictionary with a list of those categories
    
    Input:
        data (dictionary): the dataset to count
        top_num (int): the number of top category to keep

    Output:
        top_dict(dictionary): with the region as key and category list as value
    '''
    top_dict = {}
    
    for key, value in data.items():
        if key == 'Label':
            continue
        lst = sorted(range(len(value)), key=lambda i: value[i])[-(top_num + 1):]

        label = data['Label']
        val_lst = []
        for x in lst[: : -1]:
            if x != 0:
                val = label[x]
                val_lst.append((val, value[x]))
        top_dict[key] = val_lst
    
    return top_dict

def clean_pop(filename):
    '''
    take in the population data downloaded from census bureau and find 
    the most common race/ethnic group in each zip code

    Input:
        filename (string)
    
    Output:
        df (pandas dataframe)
    '''
    pop_data = pd.read_csv(filename)

    #getting the estimate number of each race/ethnic group in zipcode
    pop_data['Label (Grouping)'] = pop_data['Label (Grouping)'].str.strip()
    df = pop_data.filter(regex = '!Estimate')
    df.insert(0, 'Label', pop_data['Label (Grouping)'])
    df.rename(columns = lambda x: x.replace('ZCTA5 ',"")[:5], inplace = True)
    
    #modify the dataset to a dictionary
    df_1 = df.drop([0,2,3,4,7,12])
    data = df_1.to_dict('series')
    pop_data = {key: value.tolist() for key, value in data.items()}

    #changing the estimate number into percentage 
    for key, value in pop_data.items():
        if key == 'Label':
            continue
        else:
            for i, val in enumerate(value):
                if i == 0:
                    pop_val = str(val).replace(',','')
                    total_pop = float(pop_val)
                value[i] = float(str(val).replace(',','')) / total_pop

    #finding the most common 5 groups and make it into a dataframe         
    top_dict = find_top_race(pop_data, 5)
    data_list = [{'NAME': k, 'top_race': v} for k, v in top_dict.items()]
    df = pd.DataFrame(data_list)
    
    return df


def relabel(cat_lst):
    '''
    relabel the categories given by Yelp to fewer category

    Input: 
        cat_lst: list of category from Yelp

    Output:
        list of new category
    '''
    new_label = []
    for label in cat_lst:
        if label not in Not_Food and label not in Sub_Category:
            new_label.append(label)

    for i, label in enumerate(new_label):
        for category, lst in cate_dct.items():
            if category == 'Regional':
                continue
            if label in lst:
                new_label[i] = category

    return list(set(new_label))


def find_cat(cat_lst, new_cat):
    '''
    Categorize the restaurants based on new category, if category in new_cat, 
    return the most common one; if not, return 'other'
    Input:
        cat_lst: old category from Yelp
        new_cat: new list generated from relabel
    
    Output:
        new label
    '''
    find_label = False

    for category in cat_lst:
        for label in new_cat:
            if category == label:
                find_label = True
                return label
            
    if not find_label:
        return "other" 

def clean_rest(filename):
    '''
    Taking in the yelp data and relabel restaurants for data viz: relabeling 
    and finding the most common category of restaurant

    Input:
        filename (string)
    
    Output:
        df (pandas dataframe)
    '''
    with open(filename) as f:
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            data.append(row)
    
    counter = {}

    #counting the number of restaurants of each category in each zipcode
    for restaurant in data:

        cat_lst = eval(restaurant['categories'])
        zipcode = restaurant['zip_code']

        if zipcode not in counter:
            counter[zipcode] ={}

        new_category = relabel(cat_lst)
        restaurant['new_labels'] = new_category

        for type in new_category:
            counter[zipcode][type] = counter[zipcode].get(type, 0) + 1

    #Find the top 3 most common category in each zip code to visualize
    top_3_food = {}

    for key, value in counter.items():
        lst = sorted(value, key=lambda i: value[i])[-3:]
        top_3_food[key] = lst

    #change the label
    for restaurant in data:
        cat_lst = restaurant['new_labels']
        zipcode = restaurant['zip_code']
        new_cat = top_3_food[zipcode]
        restaurant['food_label'] = find_cat(cat_lst, new_cat)
        restaurant['regional_label'] = find_cat(cat_lst, cate_dct['Regional'])

    #write into a csv file
    headers = []
    for i, rest in enumerate(data):
        if i == 0:
            for head in rest:
                headers.append(head)

    with open('./cappyfoodies/cleaned_data/res_label.csv', 'w', newline = "") as csv_file:  
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def risk_category(entry):
    '''
    transform risk level from string to number

    Input:
        risk level (string)

    output:
        risk level (int)
    '''
    if entry == 'Risk 1 (High)':
        return 1
    
    elif entry == 'Risk 2 (Medium)':
        return 2
    
    else:
        return 3

def clean_risk(filename):
    '''
    Taking the restaurant riskness level data and calculate average risk
    of restaurants in a certain zip code (this should be run with the 
    Restaurant.csv file that is too large to put in github)

    Input:
        filename(string): the restaurant risk file to clean

    Output: 
        csv file: risk_cleaned.csv
    '''
    with open(filename) as f:
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            data.append(row)
    
    #calculating the number of restaurant and sum of risk by zipcode
    risk = {}
    counter = {}
    for restaurant in data:
        if restaurant['Results'] == 'Out of Business':
            continue
        zipcode = str(restaurant['Zip'])
        risk_r = risk_category(restaurant['Risk'])
        risk[zipcode] = risk.get(zipcode,0) + risk_r
        counter[zipcode] = counter.get(zipcode,0) + 1
    
    #convert to dataframe
    df_1 = pd.DataFrame.from_dict(counter, orient = 'index',columns = ['num_rest'])
    df_2 = pd.DataFrame.from_dict(risk, orient = 'index', columns = ['sum_risk'])
    risk_df = df_1.join(df_2)

    #calculating average risk
    risk_df['avg_risk'] = risk_df['sum_risk']/risk_df['num_rest']
    risk_df.index.name = 'NAME'
    
    risk_df.to_csv("./cappyfoodies/cleaned_data/risk_cleaned.csv")
    