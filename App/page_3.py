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

page_3_layout = html.Div([
    html.Div([
        dmc.Title("About Us", color="blue", size="h3"),
        html.Br(),
        html.Br(),
        html.Br(),
        html.H4('Université Lumière Lyon 2 - Master 2 SISE 2023-2024'),
        html.Br(),
        html.H5('Machine learning Python Project'),
        html.A('Supervised by Mr. Anthony Sardellitti'),
        html.Br(),
        html.Br(),
        html.P('Authors: Abdourahmane Ndiaye, Fiona Steiner, Nousra Chaibati'),
        html.A('GitHub project',href='https://github.com/Abdouragit/Land_value_estimation/tree/main')
],style={'margin-right':'30px','margin-left':'30px'}, className="shadow-lg p-1 mb-5 bg-white rounded")
])