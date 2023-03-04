import sys
import warnings
warnings.filterwarnings("ignore")
# from . import dashboard
# from .scraping_data.pantry_scraper import food_pantry_tbl, lat_long
# from .scraping_data.yelp_simulation import yelp_simul
# from .scraping_data.yelp_api import get_businesses, get_reviews


def run_dashboard():
    """
    Running dashboard
    """
    app = dashboard.app
    app.run_server(debug=False)

def run_pantry_scraper(): 
    """
    Running Pantry Scraper
    """
    return food_pantry_tbl()

def run_api_simulation():
    """
    Running Yelp API Simulation
    """
    return yelp_simul()

def run_yelp_restaurants():
    """
    Gather Yelp restaurants from Cook County
    """
    return get_businesses()

def run_yelp_reviews():
    """
    Gather reviews for Cook County restaurants
    """
    return get_reviews()


# def run_un_api():
#     """
#     Download UN comtrade data
#     """

#     print ("Start to create dataset.")
#     un_api.create_un_data()
#     print ("Dataset is ready.")

# def run_imf_api():
#     """
#     Download IMF data
#     """

#     print ("Start to create dataset.")
#     imf_api.create_export_import_data()
#     print ("Dataset is ready.")

# def run_loadcsv():
#     """
#     Download CSV from multisources
#     """
#     getready_data.create_csv_data()

def run():
    """
    User type some arguments and we run a program
    """
    print("Welcome to our Trade Dashboards and Analysis program!")
    user_input = input(
        """Please type 
            'dashboard' for dashboard, 
            'clean data' for cleaning data, 
            'scrape' for starting web scraping
            'quit' or anything else for quit program.""")
    if user_input == 'dashboard':
        print("running dashboard...")
        run_dashboard()
    # elif user_input == "clean data":
    #     print("running data cleaning...")
    #     run_analysis()
    elif user_input == 'scrape':
        getdata_user_input = input(
            """Please type 
                'scraper' to scrape the list of emergency pantries from
                Cook County's Sheriff's Office,
                'simulation' to simulate interacting with Yelp's API,
                'reviews' to gather the full dataset of reviews for restaurants
                in Cook County using Yelp's API, or
                'quit' or anything else for quit program.""")
        if getdata_user_input == 'scraper':
            print("Scraping data...")
            run_pantry_scraper()
        elif getdata_user_input == 'simulation':
            print("Starting Simulation...")
            run_api_simulation()
        elif getdata_user_input == 'reviews':
            print("Getting reviews")
            run_yelp_restaurants()
            run_yelp_reviews()
        else:
            sys.exit()

    else:
        sys.exit()

