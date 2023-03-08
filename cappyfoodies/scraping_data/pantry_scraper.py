'''
Written by: Maxine Xu
'''
import requests
import lxml.html
import pandas as pd

GMAP_API_KEY = "AIzaSyAKL3FqXAhlQLArA5lURGYl2cv6OTvE0LM"

def food_pantry_tbl():
    '''
    This function scrapes the Sheriff's Office's resource which lists the 
    emergency food pantries in Cook County.
        
    Outputs:
        pantry_df (Pandas DataFrame): Dataframe of emergency food pantries and 
            their information (includes location, service area, 
            and phone number)
        pantry_data.csv, which is a CSV that lists the food pantries in Cook 
            County and the information in the above DataFrame
    '''
    #URL to the Sheriff's Office's emergency pantry resource
    pantry_url = "https://www.cookcountysheriff.org/departments/courts/civil-services/evictions/social-services/emergency-food-pantries/"
    lst = []
    response = requests.get(pantry_url)
    root = lxml.html.fromstring(response.text)
    rows = root.xpath("//table/tbody/tr")

    #Appending each row of the scraped table to the list
    for row in rows:
        lst.append(row.xpath(".//td/text()"))

    #Turning list into datafame
    pantry_df = pd.DataFrame(lst[1:], columns =lst[0])

    #Cleaning Dataframe
    pantry_df["Zip"] = pantry_df['Zip'].astype('str')
    pantry_df["Full Address"] =\
     pantry_df["Address"] + ", " + pantry_df["City"] + ", " +\
      pantry_df["State"] + " " + pantry_df["Zip"]

    #Using helper function to get the longitude and latitude of each pantry
    pantry_df['Lat_Long'] = pantry_df.apply(lambda x: lat_long(
        x['Full Address']), axis=1)
    pantry_df[['Lat', 'Long']] = pd.DataFrame(pantry_df['Lat_Long'].tolist(),
     index=pantry_df.index)
    return pantry_df

def lat_long(full_address):
    '''
    This function uses the Google Maps API to get the longitude and latitude 
    of an address.

    Inputs:
         full_address (string): string of location's address 

    Outputs:
         lat, long (tuple): Tuple of the latitude and longitude
    '''
    gmap_url = "https://maps.googleapis.com/maps/api/geocode/json?"

    response = requests.get(gmap_url, params = {"key": GMAP_API_KEY, "address":
     full_address}).json()

    if response ["status"] == "OK":
        loc = response["results"][0]["geometry"]
        lat = loc["location"]["lat"]
        long = loc["location"]["lng"]
        return lat, long
    
def write_pantry_file():
    '''
    This function writes the scraped data to a CSV file.
    
    Outputs:
        pantry_data.csv, which is a CSV that lists the food pantries in Cook 
            County and the information in the above DataFrame
    '''
    pantry_data = food_pantry_tbl()
    pantry_data.to_csv('pantry_data.csv')
