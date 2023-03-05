import requests
from .yelp_api import API_KEY, BUS_ENDPOINT, HEADERS

def yelp_simul():
    '''
    This function simulates a call to Yelp Fusion's API to get a list of restaurants
    for an inputted location and the reviews for an inputted restaurant ID.
    '''
    #Simulating getting businesses
    print("To get a list of restaurants that input your zipcode or your city:")
    print("")
    print("")
    print("You could use your current zipcode. For example: 60637")
    print("")
    print("")
    print("You could also input your current city. For example: Chicago")
    print("")
    print("")
    print("Or you could input your address. For example: 5801 S Ellis Ave, Chicago, IL 60637")
    print("")
    
    #User inputs location
    location = input('Type your location here: ')
    
    #Call to Yelp's API
    PARAMETERS = {'limit': 5, 'categories': 'food', 'location': location, 'sort_by': 'rating'}
    response = requests.get(url = BUS_ENDPOINT, params = PARAMETERS, headers = HEADERS)
    try:
        bus_dic = response.json()["businesses"]        
    except Exception:
        return "Make sure your inputted location matches the formatting above and rerun!"

    #Prints businesses
    for i, bus in enumerate(bus_dic):
        print("")
        print("")
        print("#{}: {} has an average rating of {}.".format(i+1, bus['name'], bus['rating']))
        print("To get the Yelp reviews, copy and paste this ID: {}".format(bus['id']))
        print("")
    
    #Simulating yelp reviews
    print("To simulate getting a review for a restaurant, input the restuarant's Yelp unique ID.")
    print("")
    print("")
    
    #User inputs restaurant ID
    business_id = input('Copy and paste the ID here to see three Yelp reviews: ')
    
    #Call to Yelp's API
    REVIEWS_ENDPOINT = "https://api.yelp.com/v3/businesses/{}/reviews".format(business_id)
    response = requests.get(url=REVIEWS_ENDPOINT, headers = HEADERS)
    try:
        rev_dic = response.json()['reviews']       
    except Exception:
        return "Make sure your inputted business ID matches the formatting above and rerun!"

    #Prints Yelp reviews
    for i, rev in enumerate(rev_dic):
        print("")
        print("Review #{}: {}".format(i+1, rev['text']))
        print("User Rating: {}/5".format(rev['rating']))
        print("")
