# This restaurants_cleanup.py file was written by Jariel Yang
import json
import re
import ast
import pandas as pd


DROP_LIST = ["Unnamed: 0","alias", "image_url", "coordinates", "transactions",
            "phone", "display_phone"]
    

def construct_location(dataset):
    """
    Contruct "city, and state" columns for the dataset
    
    Inputs:
        dataset: pd.DataFrame
    """
    
    def get_loc(loc_text, key):# Function used to extract location from a dict-like string
        
        loc_dict = ast.literal_eval(loc_text)
        
        return loc_dict[key]
    
    dataset["city"] = dataset["location"].map(lambda loc_text: get_loc(loc_text, "city"))
    dataset["city"] = dataset["city"].map(lambda x: x.lower())
    dataset["state"] = dataset["location"].map(lambda loc_text: get_loc(loc_text, "state"))
    

def set_price_level(dataset):
    """
    Add a new column into the dataset by the dollarsign specified by each business
    example:
        each $ = 9.5 dollars
    """
    
    def cal_dollar_sign(symbol):
        
        if type(symbol) == float:
            return None
        
        if re.findall(r"\$+", symbol) != []:
            return 9.5 * len(symbol)
        
        return None
        
    dataset["price_level"] = dataset["price"].map(cal_dollar_sign)

    
def construct_zip_code(dataset):
    """
    Extract the zip code from the location string and construct a new zip code column in place
    """
    
    # Function used to extract 5-digits zip code
    def get_zip_code(text):
        
        zip_code = re.findall(r"\'\d{5}\'", text)
        
        if zip_code == []:
            return None
        
        return zip_code[0].replace("\'", "")

    dataset["zip_code"] = dataset["location"].map(get_zip_code)


def category_cleaner(dataset):
    """
    Clean the category data for each business of the dataset
    """
    
    def reset_list(cate_text): # Function used to extract info from "title"
        
        new_lst = []
        text_lst = ast.literal_eval(cate_text)
        for item in text_lst:
            new_lst.append(item["title"])
        
        return new_lst
    
    def check_is_food(cate_lst, labels):# Function used to check food categories
        
        for label in labels:
            if label in cate_lst:
                return True
        
        return False
    
    # Extract categories from the "title" in the given data
    dataset["categories"] = dataset["categories"].map(reset_list)
    
    # Load in a csv file containing labels related to food,
    # where "1" and "a" represent categories that are related to food
    labels = pd.read_csv("./cappyfoodies/data/label.csv")
    labels = labels[(labels["is_food"] == "1") | (labels["is_food"] == "a")]
    food_labels = labels["categories"]
    
    # Filter out entries with categories that are irrelevant to food
    fil_con = dataset["categories"].map(lambda cate_lst: check_is_food(cate_lst, food_labels))
    dataset = dataset[fil_con]
    
    return dataset
    

def business_cleaner(dataset):
    """
    Clean the dataset by specified state and categories
    
    Inputs:
        dataset: pd.DataFrame
    Returns: a filtered pd.DataFrame
    """
    
    # Drop unuseful columns
    new_df = dataset.drop(DROP_LIST, axis = 1)
    
    # Clean each entry of catogory column
    new_df = category_cleaner(new_df)
    
    # Set the price_level column
    set_price_level(new_df)
    
    # Set the zip_code column
    construct_zip_code(new_df)
    
    # Construct the location and change none-IL data to NA
    construct_location(new_df)
    new_df["state"][new_df["state"] != "IL"] = None
    
    # Drop rows with missing values
    new_df.dropna(axis = 0, inplace = True)

    # return restaurants that are still open
    return new_df[new_df["is_closed"] == False].reset_index(drop = True)


def df_to_csv(dataset, filename):
    """
    Write pd.dataframe to csv file
    """
    
    assert filename.endswith(".csv"), "the format should be .csv !"
    
    address = './cappyfoodies/cleaned_data'
    file_path = address + "/" + filename
    dataset.to_csv(file_path)


def run_business_clean():
    """
    Run the cleaning of business data and generate the cleaned data
    """
    
    business_dta = pd.read_csv("./cappyfoodies/data/yelp_businesses.csv")
    new_dta = business_cleaner(business_dta)
    df_to_csv(new_dta, "business_cleaned.csv")
    print("Restaurants data all cleaned !")
            

if __name__=="__main__":
    
    run_business_clean()
