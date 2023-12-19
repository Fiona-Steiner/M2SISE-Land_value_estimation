from ast import Str
from dash import Dash, dcc, html, Input, Output,callback,State,dash_table
import dash_bootstrap_components as dbc
import os,sys,subprocess
import pandas as pd 
import pathlib
import pickle
import logging
logger = logging.getLogger(__name__)
import joblib
import dash_mantine_components as dmc

import matplotlib.pyplot as plt
import geopandas as gpd
import io
import base64
import dash.dependencies as dd
import folium
from IPython.display import display

# Generate your map
def generate_map():

    # Load real estate data from a txt file
    data = pd.read_csv("Data/Land_data_clean.txt", delimiter=';', low_memory=False)
    #data2 = pd.read_csv("../Data/Dataset/Land_data_clean2.txt", delimiter=';', low_memory=False)
    #data3 = pd.read_csv("../Data/Dataset/Land_data_clean3.txt", delimiter=';', low_memory=False)

    # Concatenation of the 4 files/dataframe:
    #data = pd.concat([data1, data2, data3])
    #data

    # Selection of the column to keep
    columns_keep = ['Code departement', 'Valeur fonciere']
    data = data.loc[:, columns_keep]

    # Grouping by department
    data = data.groupby('Code departement')['Valeur fonciere'].median().reset_index()

    # Load geographic data from departments in GeoJSON format
    departements_geojson = gpd.read_file('Data/outlinesdepartments.geojson')

    # Merging our data with geographic data
    df_cartographie = pd.merge(departements_geojson, data, left_on='code', right_on='Code departement', how='inner')

    columns_keep = ['code', 'nom', 'geometry', 'Valeur fonciere']
    df_cartographie = df_cartographie.loc[:, columns_keep]

    # Create a map centered on France

    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

    # Define a color scale for the 'Valeur fonciere' values
    color_scale = folium.LinearColormap(
        colors=['white', 'orange', 'red'],
        vmin=df_cartographie['Valeur fonciere'].min(),
        vmax=df_cartographie['Valeur fonciere'].max()
    )

    # Add a GeoJSON layer to display department borders with custom colors
    folium.GeoJson(
        df_cartographie,
        style_function=lambda feature: {
            'fillColor': color_scale(feature['properties']['Valeur fonciere']),
            'color': 'black',
            'weight': 2,
            'fillOpacity': 0.7,
        },
        tooltip=folium.GeoJsonTooltip(fields=['nom', 'Valeur fonciere'], aliases=['Département', 'Valeur Foncière'], localize=True),
    ).add_to(m)

    # Add the color scale to the map
    color_scale.caption = 'Land Value (in Euros)'
    color_scale.add_to(m)

    m.save('folium_map.html')

generate_map()

page_2_layout = html.Div([
    html.Div([
    #html.H3('French land values Map',style={'margin-left':'30px','color':'black'}),
    dmc.Title("Land Values Map", color="blue", size="h3"),
    html.P('Average land value per department (in Euros)'),
    ],style={'margin-right':'30px','margin-left':'30px'}, className="shadow-lg p-1 mb-5 bg-white rounded"),
    
    html.Div([
            #html.Label("Mapping of land value means"),
            html.Iframe(id='map', srcDoc=open('folium_map.html', 'r').read(), width='100%', height='600')
    ],style={'margin-right':'30px','margin-left':'30px'}, className="shadow-lg p-1 mb-5 bg-white rounded"),
    
])
