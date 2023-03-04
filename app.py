import sys
import warnings
warnings.filterwarnings("ignore")
from . import dashboard
from .scraping_data import <getready_data, imf_api, un_api>


def run_dashboard():
    """
    Running dashboard
    """
    app = dashboard.app
    app.run_server(debug=False)


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
    elif user_input == "clean data":
        print("running data cleaning...")
        run_analysis()
    elif user_input == 'scrape':
        getdata_user_input = input(
            """Please type 
                'unapi' for download un api,
                'imfapi' for download imf api,
                'loadcsv' for download and clean WTO trade products, 
                    OWID covid, World Bank econ data and Country code data, 
                'quit' or anything else for quit program.""")
        if getdata_user_input == 'unapi':
            print("getting new data...")
            run_un_api()
        elif getdata_user_input == 'imfapi':
            print("getting new data...")
            run_imf_api()
        elif getdata_user_input == 'loadcsv':
            print("getting new data...")
            run_loadcsv()
        else:
            sys.exit()
    else:
        sys.exit()