import pandas as pd
import geojson
import folium
from folium.plugins import MarkerCluster
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash.dependencies import Input, Output
import json
import numpy as np
from wordcloud import WordCloud
from PIL import Image
from dash import html, dcc
from io import BytesIO
import base64
from nltk.corpus import stopwords
import pathlib

res_label = pathlib.Path(__file__).parent / "../cleaned_data/res_label.csv"
pantry_data = pathlib.Path(__file__).parent / "../cleaned_data/pantry_data.csv"
res_riskiness = pathlib.Path(__file__).parent / "../cleaned_data/risk_cleaned.csv"
demo_data = pathlib.Path(__file__).parent / "../cleaned_data/demo_data.csv"
business_cleaned_v3 = pathlib.Path(__file__).parent / "../cleaned_data/business_cleaned_v3.csv"
boundaries = pathlib.Path(__file__).parent / "../cleaned_data/Boundaries - ZIP Codes.geojson"
cleaned_review = pathlib.Path(__file__).parent / "../cleaned_data/cleaned_review_V2.json"

df_restaurants_yelp = pd.read_csv(res_label)
df_pantries = pd.read_csv(pantry_data)
df_foodrisk_byzip = pd.read_csv(res_riskiness)
demo_data =  pd.read_csv(demo_data)
business_dta = pd.read_csv(business_cleaned_v3)

with open(cleaned_review) as f:
    review_dta = json.loads(f.read())

with open(boundaries) as f:
    gj = geojson.load(f)

# Merge restaurant and risk data
merged_restaurant = pd.merge(df_restaurants_yelp, df_foodrisk_byzip, left_on='zip_code', right_on='NAME')


def map_zipcode_with_id(dataset):
    """
    Compuate a dictionary where the key is the zip code and the value is 
    a list of corresponding ids.
    
    Inputs:
        dataset: a pandas,DataFrame
    Outputs:
        zipcode_dict: a dictionary
    """
    
    zipcode_dict = dict()
    
    for zip_code in dataset["zip_code"].unique():
        res_id = dataset["id"][dataset["zip_code"] == zip_code]
        zipcode_dict[zip_code] = list(res_id)
    
    return zipcode_dict


def cluster_tokens(zipcode_dict, review_dta):
    """
    Cluster the tokens together by the zip code
    
    Inputs:
        zipcode_dict: a dictionary where the key is the zip code and the value is 
        a list of corresponding ids
        review_dta: a dictionary containing restaurants' reviews
    Outputs:
        zipcode_tokens: a dict mapping zip code to the tokens of all restaurants
        within this region
    """
    
    zipcode_tokens = dict()
    
    for zip_code, id_lst in zipcode_dict.items():
        all_tokens = list()
        
        for res_id in id_lst:
            all_tokens.extend(review_dta[res_id]["tokens"])
            
        zipcode_tokens[zip_code] = all_tokens
    
    return zipcode_tokens


def gene_token_freq(token_lst):
    """
    Generate a dictionary where key is the token and the value is the counts
    of its occurence.
    
    Inputs:
        token_lst: a list of strings
    Outputs:
        token_freq: a dictionary
    """
    
    token_freq = dict()
    
    for token in token_lst:
        if not token in token_freq.keys():
            token_freq[token] = 1
        else:
            token_freq[token] += 1
    
    return token_freq


def plot_wordcloud(token_freq):
    """
    Plot a word cloud based on the frequency data
    
    Inputs:
        token_freq: a dictionary where key is the token and the value is the counts
        of its occurence
    Outputs: a word cloud picture
    """
    
    plate_mask = np.array(Image.open("plate2.jpeg"))
    wc = WordCloud(background_color='white', 
                   width=40, 
                   height=30, 
                   mask=plate_mask)
    wc.fit_words(token_freq)
    
    return wc.to_image()

#functions for word cloud
zipcode_dict = map_zipcode_with_id(business_dta)
zipcode_tokens = cluster_tokens(zipcode_dict, review_dta)

#functions in order to make bar chart
df = demo_data.iloc[0:1]
race_info = eval(df['top_race'].tolist()[0])
race_lst = []
perc_lst = []

for tuple in race_info:
    race, perc = tuple
    race_lst.append(race)
    perc_lst.append(perc)

data = {'Race': race_lst,
        'Percentage': perc_lst}
df = pd.DataFrame(data)

def bar_plot(zipcode,demo_data):
    '''
    Taking in the demographic info of a zipcode and return the bar plot
    Input:
        zip code (int): zip code of area of interest
        demo_data: the dataset containing info
    
    Output:
        figure
    '''
    row = demo_data.loc[demo_data['NAME'] == zipcode] #change the type to str
    race_info = eval(row['top_race'].tolist()[0])
    race_lst = []
    perc_lst = []
    
    for tuple in race_info:
        race, perc = tuple
        race_lst.append(race)
        perc_lst.append(perc)

    data = {'Race': race_lst,
            'Percentage': perc_lst}
    
    row = pd.DataFrame(data)
    
    fig = px.bar(row, x = "Race", y = 'Percentage')
    
    return fig


zip_lst = []
for i in df_foodrisk_byzip['NAME']:
        zip_lst.append(i)
zip_lst = zip_lst[0:59]

colors = {
    'background': '#FDFEFE',
    'text': '#17202A'
}

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# Define initial dropdown option
initial_selection = 'restaurants'

# Define dropdown options
dropdown_options = [
    {'label': 'Restaurants', 'value': 'restaurants'},
    {'label': 'Food Pantries', 'value': 'pantries'}
]

#Main cook county map
map = folium.Map(location=[41.808611, -87.888889], default_zoom_start=12)

# Add choropleth layer to the map
folium.Choropleth(
    geo_data=gj,
    data=merged_restaurant,
    columns=['zip_code', 'avg_risk'],
    key_on='feature.properties.zip',
    fill_color='RdBu',
    fill_opacity=0.7,
    line_opacity=0.7,
    legend_name='Average Risk Score',
    highlight=True,
).add_to(map)

# Add a marker for every restaurant in the yelp dataset
marker_cluster = MarkerCluster().add_to(map)
for i in range(merged_restaurant.shape[0]):
    location = [merged_restaurant['Lat'][i],merged_restaurant['Long'][i]]
    tooltip = "Zipcode:{}<br> name: {}<br>".format(merged_restaurant["zip_code"][i], merged_restaurant['name'][i])
    
    folium.Marker(location, 
                  tooltip=tooltip).add_to(marker_cluster)

# Add a marker for every pantry in the pantry dataset
for i in range(df_pantries.shape[0]):
    location = [df_pantries['Lat'][i],df_pantries['Long'][i]]
    tooltip = "Zipcode:{}<br> Organization: {}<br>".format(df_pantries["Zip"][i], df_pantries['Organization'][i])
    
    folium.Marker(location,
                  tooltip=tooltip).add_to(marker_cluster)

#App
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
# Define the layout
app.layout = html.Div(style={'backgroundColor': colors['background']}, 
                      children=[

    html.H1(
        children='Food Security and Accessibility in Cook County',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='''This project focuses on a variety of topics related to food accessibility and food options in Cook County, 
    Illinois, including health risk level and review of restaurants, access to free food pantry, restaurants’ category, as well as 
    related regional demographic information. This project aims to give a general description and raise awareness of how Cook County
    is meeting residents' demand for food, clean food, and food of the quality and category they desire. ''',
    
             style={
        'textAlign': 'center',
        'color': colors['text'],
        'width' : '100%',
        'padding' :5
    }),
                          
    html.H2(
        children='Food Security in Cook County',
        style={
            'textAlign': 'left',
            'color': colors['text']
        }
    ), 
    html.Div(children=[
    html.H1(
        children='Demographic Information by Zipcode',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.H3(id = 'income',
        style={
        'textAlign': 'left',
        'color': colors['text']
    }),
    
    html.H3(id = 'education',
        style={
        'textAlign': 'left',
        'color': colors['text']
    }),
    
    html.H3(id = 'foodstamp',
        style={
        'textAlign': 'left',
        'color': colors['text']
    }), html.Br(),
    html.H4(children='Racial Composition (higheset percentage)'),
    dcc.Dropdown(id='zipcode-dropdown',
                 options=zip_lst,
                 value = 60637
                 ),
                 dcc.Graph(
    id='bar-graph'
    ),
    html.H3(children='Word Cloud of the most frequent words in the reviews of restaurants in this zip code',
            style={
    'textAlign': 'left',
    'color': colors['text'],
    'width':'80%',
    'padding' :10, 
    }),
    html.Img(id="image_wc", width = "500", height = "500")]
    , className='row' 
    , style={'width': '47%', "vertical-align":"top", "float":"right",'backgroundColor': colors['background']})
    , html.Div(children='''This graph demonstrates the number of restaurants and their average risk to public health by zip code. 
    The heat map shows the distribution of risk of adversely affecting the public's health across Cook County, on a scale of 1 
    (Red) being high risk and 3 (Blue) being low risk. The bubbles give the number of restaurants in that region.''',
    style={
    'textAlign': 'left',
    'color': colors['text'],
    'width' : '50%',
    'padding' : 5
    }),
    html.Iframe(
    id='map',
    srcDoc=map._repr_html_(),
    width='50%',
    height='500'
    ),
    html.Br(),
    html.Br(),
    html.H2(
    children='Food Accessibility in Cook County',
    style={
    'textAlign': 'left',
    'color': colors['text']
    }
    ),
    html.Div(children='This graph gives the geographic location of pantries and restaurants. The pantry submap gives information of where \
             to find food pantry and its serve area. The restaurant submap has a slider with which the user can filter restaurants by their \
             rating (from 1 - 5)  on Yelp. At the same time, the restaurants are color-coded if they serve one of the most common regional/ethnic foods.',
             style={
    'textAlign': 'left',
    'color': colors['text'],
    'width':'50%',
    'padding' :10, 
    }), 
    html.Br(),
    html.Br(),
    html.Div(children='''Choose the dataset'''),
    html.Div([
    dcc.Dropdown(
    id='dropdown',
    options=dropdown_options,
    value=initial_selection
    ),
    html.Br(),
    html.Br(),
    html.Div(children='''Rating of the restaurants'''),
    dcc.Slider(
    id='rating-slider',
    min=0,
    max=5,
    step=0.5,
    value=2.5,
    marks={
    0: '0',
    1: '1',
    2: '2',
    3: '3',
    4: '4',
    5: '5'
    }),
    dcc.Graph(id='map2') 
    ], style={'width': '50%', 'display': 'inline-block'}) 
    ])

# Define the callback function
@app.callback(
        Output('map2', 'figure'),
        Input('dropdown', 'value'),
        Input('rating-slider', 'value')
        )

def update_figure(selected_option, slider_value):
    if selected_option == 'restaurants':
        filtered_df = merged_restaurant[merged_restaurant['rating'] >= slider_value]
        fig = px.scatter_mapbox(
            filtered_df,
            lat='Lat',
            lon='Long',
            color='regional_label',
            color_discrete_sequence=px.colors.qualitative.Dark24,
            mapbox_style='open-street-map',
            zoom=10,
            height=600,
            opacity=0.8,
            size_max=10
        )
    else:
        fig = px.scatter_mapbox(
            df_pantries,
            lat='Lat',
            lon='Long',
            color='Service Area',
            color_discrete_sequence=px.colors.qualitative.Dark24,
            mapbox_style='open-street-map',
            zoom=10,
            height=600,
            opacity=0.8,
            size_max=10
        )
    return fig

@app.callback(
        Output(component_id='bar-graph', component_property='figure'),
        Input(component_id="zipcode-dropdown", component_property='value')
        )
    
def update_figure(selected_zipcode):
    row = demo_data.loc[demo_data['NAME'] == selected_zipcode] #change the type to str
    race_info = eval(row['top_race'].tolist()[0])
    race_lst = []
    perc_lst = []
    
    for tuple in race_info:
        race, perc = tuple
        race_lst.append(race)
        perc_lst.append(perc)

    data = {'Race': race_lst,
            'Percentage': perc_lst}
    
    row = pd.DataFrame(data)
    
    fig = px.bar(row, x = "Race", y = 'Percentage')
    
    fig.update_layout(transition_duration=500)

    return fig

@app.callback(
        Output('image_wc', 'src'), 
        Input("zipcode-dropdown", 'value')
        )

def make_image(zip_code):
    img = BytesIO()
    token_lst = zipcode_tokens[int(zip_code)]
    plot_wordcloud(gene_token_freq(token_lst)).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

@app.callback(
        Output(component_id = 'education', component_property ='children'),
        Input(component_id="zipcode-dropdown", component_property='value')
        )

def update_output_educ(selected_zipcode):
    row = demo_data.loc[demo_data['NAME'] == selected_zipcode]
    per_bachelor = round(float(row['per_bachelor'])*100,2)
    
    return "Education: {}% have bachelor degree or higher".format(per_bachelor)

@app.callback(
        Output(component_id = 'foodstamp', component_property ='children'),
        Input(component_id="zipcode-dropdown", component_property='value')
        )

def update_output_food(selected_zipcode):
    row = demo_data.loc[demo_data['NAME'] == selected_zipcode]
    fd_stamp = round(float(row['per_fdstamp'])*100,2)
    
    return "Food stamp: {}% households are eligible for food stamp".format(fd_stamp)

@app.callback(
    Output(component_id = 'income', component_property ='children'),
    Input(component_id="zipcode-dropdown", component_property='value'))

def update_output_inc(selected_zipcode):
    row = demo_data.loc[demo_data['NAME'] == selected_zipcode]
    median_income = float(row['med_hd_inc'].str.replace(',',''))

    return "Median Household Income: ${}".format(median_income)