[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9908027&assignment_repo_type=AssignmentRepo)

# Food Accessibility and Security in Cook County

According to the United States Department of Agriculture, food insecurity is “a household-level economic and social condition of limited or uncertain access to adequate food” (USDA). For our project, we visualize and explore patterns between the following key components affecting food insecurity:

Food Access (Proximity to food)\
Food Quality \
Food Price\
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

    (1) For Dashboard, \
    (2) For data cleaning, \
    (3) Download new data,\
    (4) Quit program.

7. Option 3 has three sub-options. Users can input the number to interact with the App
    (1) Scrape the list of emergency pantries from Cook County's Sheriff's Office,\
    (2) Simulate interacting with Yelp's API,\
    (3) Gather the full dataset of reviews for restaurants in Cook County using Yelp's API


