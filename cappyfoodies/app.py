import sys
import warnings
warnings.filterwarnings("ignore")
from .dashboard import dashboard
from .scraping_data.pantry_scraper import food_pantry_tbl, lat_long
from .scraping_data.yelp_simulation import yelp_simul
from .scraping_data.yelp_api import get_businesses, get_reviews


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

def run_yelp_reviews():
    """
    Gather reviews for Cook County restaurants
    """
    get_businesses()
    return get_reviews()

def run_clean():
    """
    Clean datasets in the data directory
    """
    pass

def run():
    """
    User type some arguments and we run a program
    """
    print("Welcome to Cook County Food Accessibility and Security App!")
    user_input = input(
        """Please type 
            Please Enter: 
                (1) For Dashboard, 
                (2) For data cleaning, 
                (3) Download new data
                (4) Quit program.
                Option: """)
    if user_input == 1:
        print("running dashboard...")
        run_dashboard()
    elif user_input == 2:
        print("running data cleaning...")
        run_clean()
    elif user_input == 3:
        getdata_user_input = input(
            """Please type 
                (1) Scrape the list of emergency pantries from Cook County's Sheriff's Office,
                (2) Simulate interacting with Yelp's API,
                (3) gather the full dataset of reviews for restaurants
                in Cook County using Yelp's API, or
                (4) or anything else for quit program.""")
        if getdata_user_input == 1:
            print("Scraping data...")
            run_pantry_scraper()
        elif getdata_user_input == 2:
            print("Starting Simulation...")
            run_api_simulation()
        elif getdata_user_input == 3:
            print("Getting reviews")
            run_yelp_reviews()
        else:
            sys.exit()

    else:
        sys.exit()

