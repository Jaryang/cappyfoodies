import json
import requests
import pandas as pd

#list of zip codes in Cook County
cook_zip = ['60629',
 '60618',
 '60639',
 '60632',
 '60647',
 '60804',
 '60623',
 '60617',
 '60625',
 '60608',
 '60634',
 '60614',
 '60657',
 '60620',
 '60640',
 '60641',
 '60628',
 '60609',
 '60651',
 '60402',
 '60638',
 '60619',
 '60411',
 '60630',
 '60453',
 '60016',
 '60056',
 '60622',
 '60613',
 '60120',
 '60010',
 '60004',
 '60626',
 '60616',
 '60649',
 '60643',
 '60645',
 '60644',
 '60193',
 '60637',
 '60660',
 '60707',
 '60659',
 '60107',
 '60062',
 '60067',
 '60652',
 '60615',
 '60610',
 '60462',
 '60133',
 '60477',
 '60025',
 '60169',
 '60074',
 '60103',
 '60068',
 '60090',
 '60089',
 '60201',
 '60409',
 '60624',
 '60612',
 '60611',
 '60007',
 '60202',
 '60636',
 '60302',
 '60653',
 '60631',
 '60714',
 '60076',
 '60525',
 '60438',
 '60005',
 '60646',
 '60607',
 '60621',
 '60527',
 '60605',
 '60018',
 '60655',
 '60827',
 '60077',
 '60467',
 '60091',
 '60459',
 '60160',
 '60487',
 '60473',
 '60452',
 '60426',
 '60153',
 '60406',
 '60053',
 '60706',
 '60439',
 '60656',
 '60172',
 '60443',
 '60419',
 '60642',
 '60131',
 '60803',
 '60008',
 '60466',
 '60654',
 '60805',
 '60093',
 '60104',
 '60513',
 '60164',
 '60430',
 '60521',
 '60304',
 '60118',
 '60455',
 '60429',
 '60445',
 '60465',
 '60546',
 '60601',
 '60070',
 '60154',
 '60457',
 '60633',
 '60478',
 '60173',
 '60463',
 '60415',
 '60026',
 '60458',
 '60526',
 '60192',
 '60428',
 '60130',
 '60558',
 '60712',
 '60176',
 '60501',
 '60422',
 '60471',
 '60418',
 '60305',
 '60482',
 '60534',
 '60464',
 '60661',
 '60171',
 '60475',
 '60022',
 '60162',
 '60155',
 '60425',
 '60480',
 '60461',
 '60606',
 '60469',
 '60472',
 '60163',
 '60165',
 '60195',
 '60456',
 '60208',
 '60203',
 '60194',
 '60476',
 '60043',
 '60301',
 '60603',
 '60666',
 '60602',
 '60604',
 '60029',
 '60141',
 '60196',
 '60669',
 '60209',
 '60290',
 '60006',
 '60009',
 '60011',
 '60017',
 '60019',
 '60038',
 '60055',
 '60065',
 '60078',
 '60082',
 '60094',
 '60095',
 '60105',
 '60159',
 '60161',
 '60168',
 '60179',
 '60204',
 '60303',
 '60398',
 '60412',
 '60454',
 '60499',
 '60597',
 '60664',
 '60663',
 '60668',
 '60670',
 '60674',
 '60673',
 '60677',
 '60675',
 '60679',
 '60678',
 '60681',
 '60680',
 '60684',
 '60682',
 '60686',
 '60685',
 '60688',
 '60687',
 '60690',
 '60689',
 '60693',
 '60691',
 '60695',
 '60694',
 '60697',
 '60696',
 '60701']

API_KEY = 'g5LKgbWTyQWTEkfnknhTvgtiDMUKzp7_0v9ofFnucn7Lheiq2hTFNn2H8JRSM--SBq5RaJaKVgRqZBrJsOnWsZFvaFTAq96ADWOY5Dany9m6n7AGIzfo4cMJNOnrY3Yx'
BUS_ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'bearer %s' % API_KEY}

#Yelp labels each restaurant's price level with the following $, $$, $$$, or 
#$$$$, which translates to 1,2,3,4 in their API
price = [1,2,3,4]

def get_businesses():
    '''
    This function uses the Yelp Fusion API to get information about restaurants 
    at differing price points in Cook County.

    Outputs (CSV file):
        yelp_businesses.csv, which is a CSV file that lists the restaurant in each 
         zipcode.
    '''
    business_data = []
    #The Yelp Fusion's limit for calling businesses is 50, so in order to 
    #maximize the number of restaurants, we loop through each zipcode and each 
    #price level
 
    for zipcode in cook_zip:
        for p in price:
            #The 'rating' sort according to Yelp, "is not strictly sorted by 
            #the rating value, but by an adjusted rating value that takes into 
            #account the number of ratings"
            PARAMETERS = {'limit': 50, 'categories': 'Restaurants', 
            'location': zipcode, 'price': p, 'sort_by': 'rating'}
            response = requests.get(url = BUS_ENDPOINT, params = PARAMETERS, 
            headers = HEADERS)
      
            #Adding the dictionary of the business' information to the list
            try:
                business_data += response.json()["businesses"]
          
            #If there are no restaurants in the zipcode or at a certain 
            #price level, then pass the loop
            except Exception:
                pass
          
    business_data = pd.DataFrame.from_dict(business_data)
 
    #Removing the overlapping restaurants that appeared in the API calls
    business_data.drop_duplicates(subset=['id'])
 
    business_data.to_csv('yelp_businesses.csv')
    return business_data


def get_reviews(bus_data=None, first_round=True, round_num=''):
    '''
    This function uses the Yelp Fusion API to get the reviews for restaurants 
    in Cook County 

    Inputs:
        bus_data (list): list of business IDs, default is set to None
        first_round (boolean): True if this is the first round of API calls, 
            False otherwise
        round_num (str): String of the current round number 

    Outputs:
        final_dic: a dictionary with the key being the unique ID for each 
            restaurant and the values being the three reviews from Yelp's Fusion API
        uncleaned_yelp_reviews.json: a JSON file that contains all the reviews 
            within the above dictionary.
    '''
    final_dic = {}
 
    #Getting the business IDs of yelp businesses in the first round
    if first_round:
        business_data = pd.read_csv('yelp_businesses.csv', index_col=0)  
        bus_data = business_data['id'].tolist()
 
    #Looping through the list of business IDS and making a call to Yelp's API 
    #to get reviews for each restaurant
    for bus_id in bus_data:
        REVIEWS_ENDPOINT =\
        "https://api.yelp.com/v3/businesses/{}/reviews".format(bus_id)
        response = requests.get(url=REVIEWS_ENDPOINT, headers = HEADERS)
        try:
            final_dic[bus_id] = response.json()['reviews']
       
        #If there are no reviews for the restaurant, then pass the loop
        except Exception:
            pass
      
    with open("uncleaned_yelp_reviews.json", "w") as outfile:
        json.dump(final_dic, outfile)
    return final_dic


def get_more_revs(round_num):
    '''
    This function gets the reviews for restaurants that were missed in previous
    rounds because of the API limit.

    Inputs:
        round_num(string): String of the current round number 

    Outputs:
        'uncleaned_yelp_reviews.json', which is the overwritten JSON file that 
            contains all the reviews gotten in the current and past rounds of API 
            calls 
    '''
    #Loading the yelp reviews from previous rounds
    with open("uncleaned_yelp_reviews.json", "r") as file:
        rev_dic = json.load(file)
    
    #Getting the business IDs that we already have reviews for and subtracting
    #it from the total list of business IDs to find the businesses we don't 
    #have reviews for
    bus_with_revs = list(rev_dic.keys())
    business_data = pd.read_csv('yelp_businesses.csv', index_col=0)
    business_ids = business_data['id'].tolist()
    bus_without_revs = list(set(business_ids) - set(bus_with_revs))
    
    #Getting the reviews and adding them to the original dictionary. 
    more_revs = get_reviews(bus_without_revs, False, round_num)
    rev_dic.update(more_revs)
    
    #Overwriting the file to include the yelp reviews from past reviews and 
    #the current one
    with open("uncleaned_yelp_reviews.json", "w") as outfile:
        json.dump(rev_dic, outfile)
