import pandas as pd
import re
import csv

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

def relabel(cat_lst):
    cate_dct = {
    'Bakeries' : ["Bakeries", "Piadina", "Pretzels", "Bagels", 'Patisserie/Cake Shop'],
    'Alcohol' : ['Cocktail Bars','Brewpubs','Beer Bar','Whiskey Bars','Wine Bars','Beer, Wine & Spirits', 'Pubs', 'Bars','Dive Bars', \
                 'Sports Bars','Beer', 'Wine & Spirits', 'Breweries', 'Cideries', 'Distilleries', 'Meaderies', 'Wineries', 'Wine Tasting Room'],
    'Coffee_Tea' : ['Coffee & Tea','Coffee Roasteries', 'Tea Rooms,Bubble Tea', 'Cafes'],
    'Dessert' : ['Candy Stores','Pancakes','Desserts','Chimney Cakes','Cupcakes','Custom Cakes','Donuts', 'Gelato', 'Honey', \
                 'Ice Cream & Frozen Yogurt', 'Milkshake Bars', 'Shaved Ice', 'Shaved Snow', 'Candy Stores', 'Chocolatiers & Shops', 'Macarons'],
    'Grocery' : ['Imported Food', 'International Grocery','Organic Stores','Fruits & Veggies','Health Markets','Convenience Stores','Farmers Market','CSA'],
    'Beverage' : ['Juice Bars & Smoothies', 'Acai Bowls','Kombucha', 'Water Stores', 'Bubble Tea'],
    'Fast_Food': ['Burgers', 'Chicken Wings','Fast Food','Pizza', 'Hot Dogs', 'Sandwiches'],
    'Specialty_Store' : ['Cheese Shops','Herbs & Spices','Olive Oil','Pasta Shops','Popcorn Shops','Tofu Shops','Empanadas'],
    'Meat_Shop' : ['Seafood Markets', 'Butcher', 'Smokehouse'],
    'Regional' : ['Cuban','Venezuelan','Honduran','Vietnamese','Afghan','African','Bulgarian','Colombian', 'Japanese', 'Laotian', 'Latin American', \
                  'Mediterranean', 'Mexican', 'Middle Eastern', 'Modern European', 'New Mexican Cuisine', 'Pakistani','Pan Asian', 'Polish', 'Puerto Rican', 'Scottish', \
                  'Southern','Thai', 'Turkish','Chinese', 'Czech','Filipino','French','Greek', 'Hawaiian', 'Indian', 'Irish', 'Korean','German','Italian',\
                  'Japanese','Czech','American (Traditional)','American (New)','Asian Fusion', 'Cajun/Creole','Cantonese','Caribbean']
    }
    Not_Food = ['Kids Activities','Music Venues','Arcades','Venues & Event Spaces','Party & Event Planning','Comedy Clubs','Bookstores','Lounges', 'Vape Shops','Gift Shops']
    for label in cat_lst:
        if label in Not_Food:
            cat_lst.remove(label)

    for i, label in enumerate(cat_lst):
        for category, lst in cate_dct.items():
            if label in lst:
                cat_lst[i] = category
        
    return list(set(cat_lst))

def clean_rest(filename):

    with open(filename) as f:
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            data.append(row)
    
    counter = {}

    for restaurant in data:
        cat_lst = eval(restaurant['categories'])
        zipcode = restaurant['zip_code']
        if zipcode not in counter:
            counter[zipcode] ={}
        relabel_lst = relabel(cat_lst)
        for type in relabel_lst:
            counter[zipcode][type] = counter[zipcode].get(type, 0) + 1


    top_5_food = {}
    sum_lst = []

    for key, value in counter.items():
        #change to modify top ones to have
        lst = sorted(value, key=lambda i: value[i])[-3:]
        sum_lst.extend(lst)
        top_5_food[key] = lst
    
    return top_5_food


