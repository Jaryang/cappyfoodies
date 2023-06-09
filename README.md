[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9908027&assignment_repo_type=AssignmentRepo)

# Food Accessibility and Security in Cook County

According to the United States Department of Agriculture, food insecurity is “a household-level economic and social condition of limited or uncertain access to adequate food” (USDA). For our project, we visualize and explore patterns between the following key components affecting food insecurity:

Food Access (Proximity to food)\
Food Quality \
Food Type\
Restaurant Cleanliness\
Socioeconomic Factors

Our project centers on Cook County and uses data from Yelp Fusion’s API, scraped emergency pantry data from the Sheriff’s Office’s, and downloaded demographic data from the US Census Bureau. 

Since 1 in 4 children in Cook County are at risk of hunger, we hope that our application can help educate people about food accessibility as it is a critical health issue.

### Team Member (Last Name in Alphabetic Order)
Miao Li, Yueyue Wang, Maxine Xu, Jariel Yang

### Package used
pandas \
geojson\
folium\
plotly\
dash\
json\
numpy\
wordcloud\
PIL\
io\
base64\
nltk\
pathlib

### Data Source

(1) Yelp API:\
Source: Yelp.com\
Way of Collection: Ask for access\
Members responsible: Maxine and Jariel

(2) Emergency Food Pantries:\
Source: Cook County’s Sheriff's Office \
(https://www.cookcountysheriff.org/departments/courts/civil-services/evictions/social-services/emergency-food-pantries/) \
Way of Collection: Web-scraping \
Members responsible: Maxine

(3)Education Data:\
Source: US Census Bureau \
(https://data.census.gov/table?t=Educational+Attainment&g=0500000US17031$8600000) \
Way of Collection:  Directly downloaded the CSV\
Members responsible: Miao 

(4) Food Stamp Data:\
Source: US Census Bureau \
(https://data.census.gov/table?t=SNAP/Food+Stamps&g=0500000US17031$8600000) \
Way of Collection:  Directly downloaded the CSV\
Members responsible: Miao

(5) Income Data:\
Source: US Census Bureau \
(https://data.census.gov/table?t=Earnings (Individuals):Income(Households,+Families,+Individuals):Income+and+Earnings:SNAP/Food+Stamps&g=0500000US17031$8600000) \
Way of Collection:  Directly downloaded the CSV\
Members responsible: Miao

(6) Race Data:\
Source: US Census Bureau \
(https://data.census.gov/table?t=Populations+and+People&g=0500000US17031$8600000&tid=ACSDP5Y2021.DP05) \
Way of Collection: Directly downloaded the CSV \
Members responsible: Miao

(7) Restaurant by zipcode:\
Souce: Chicago open data portal \
(https://data.cityofchicago.org/Health-Human-Services/Restaurant/5udb-dr6f/data) \
Way of Collection: Directly downloaded the CSV \
Members responsible: Miao

(8) Cook County Boundary geojson file:\
Souce: Cook county government\
(https://www.cookcountyil.gov/CookCentral) \
Way of Collection: Directly downloaded the geojson \
Members responsible: Yueyue 

# Steps to launch the application

1. Clone the repository.
```
git clone git@github.com:uchicago-capp122-spring23/30122-project-cappyfoodies.git
```
2. Navigate to the repository.
```
cd ./30122-project-cappyfoodies
```
3. Establish Dependencies.
```
poetry install
```
4. Activate the virtual environment.
```
poetry shell
```
5. Launch the App
```
python3 -m cappyfoodies
```
6. Options of the App. Users can enter the option number to interact with the App

    (1) The Dashboard, \
    (2) Data Cleaning, \
    (3) Scraping Data and API Interaction, \
    (4) Quit program.

7. Option 3 has three sub-options. Users can input the number to interact with the API or do web scraping

   Notes: \
   Since Yelp has a maximum number of 5,000 calls/day, run (2) before running (3) \
   A Google Maps API key is needed to run (1) \
   A Yelp Fusion API Key is needed to run (2) and (3)
   
    (1) Scrape the list of emergency pantries from Cook County's Sheriff's Office, \
    (2) Simulate interacting with Yelp's API ,\
    (3) Gather the full dataset of reviews for restaurants in Cook County using Yelp's API

### Dashboard Example
<img width="543" alt="Screen Shot 2023-04-16 at 6 31 50 PM" src="https://user-images.githubusercontent.com/111720298/232349818-fb523756-7d86-4369-b9a2-5fe0d5df890e.png">


