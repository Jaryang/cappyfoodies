import sys
from .dashboard import main_dash_after_style
from .scraping_data.pantry_scraper import food_pantry_tbl
from .scraping_data.yelp_simulation import yelp_simul
from .scraping_data.yelp_api import get_businesses, get_reviews
from .clean_func.gen_data import gen_data


def run_dashboard():
    """
    Running dashboard
    """
    app = main_dash_after_style.app
    app.run_server(debug=False)

def run_pantry_scraper(): 
    """
    Running Pantry Scraper
    Written by: Maxine Xu
    """
    return food_pantry_tbl()

def run_api_simulation():
    """
    Running Yelp API Simulation
    Written by: Maxine Xu
    """
    return yelp_simul()

def run_yelp_reviews():
    """
    Gather reviews for Cook County restaurants
    Written by: Maxine Xu
    """
    get_businesses()
    return get_reviews()

def run_clean():
    """
    Clean datasets in the data directory
    Written by: Miao Li
    """
    gen_data()

def run():
    """
    User type some arguments and we run a program
    """
    print("Welcome to Cook County Food Accessibility and Security App!")
    user_input = input(
        """Please Enter: 
                (1) For Dashboard, 
                (2) For Data Cleaning, 
                (3) For Scraping Data and API Interaction
                (4) Quit App.
                Option: """)
    if user_input == "1":
        print("running dashboard...")
        run_dashboard()
    elif user_input == "2":
        print("running data cleaning...")
        run_clean()
    elif user_input == "3":
        getdata_user_input = input(
            """Please Enter 
                (1) Scrape the list of emergency pantries from Cook County's Sheriff's Office,
                (2) Simulate interacting with Yelp's API,
                (3) Gather the full dataset of reviews for restaurants
                in Cook County using Yelp's API, or
                (4) Or anything else for quit program.
                Option: """)
        if getdata_user_input == "1":
            print("Scraping data...")
            print(run_pantry_scraper())
        elif getdata_user_input == "2":
            print("Starting Simulation...")
            run_api_simulation()
        elif getdata_user_input == "3":
            print("Getting reviews...")
            run_yelp_reviews()
        else:
            sys.exit()

    else:
        sys.exit()

