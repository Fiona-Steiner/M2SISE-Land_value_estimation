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

# Incorporate data
data = pd.read_csv('Data/Land_data_clean.txt', delimiter=';', low_memory=False)

# Définir les valeurs initiales des filtres
initial_commune_selection = ['LYON 1ER']
initial_local_type_selection = ['Maison', 'Appartement']


page_1_layout = html.Div([
    html.Br(),
    dmc.Container([
    html.Div([
        dmc.Title("Land Value Dashboard", color="blue", size="h3"),
        html.Br(),
        dmc.Grid([
                html.Div([
                html.Label("Filter by municipality"),
                dcc.Dropdown(
                    id='commune-filter',
                    options=[{'label': commune, 'value': commune} for commune in data['Commune'].unique()],
                    multi=True,
                    value=initial_commune_selection  # Valeurs initiales
                )
            ],style={'margin-right':'30px'}, className="shadow-lg p-1 mb-5 bg-white rounded"),

                html.Div([
                html.Label("Filter by Type local"),
                dcc.Dropdown(
                    id='type-local-filter',
                    options=[{'label': local_type, 'value': local_type} for local_type in data['Type local'].unique()],
                    multi=True,
                    value=initial_local_type_selection  # Valeurs initiales
                )
            ], className="shadow-lg p-1 mb-5 bg-white rounded"),
        ]),
    ],style={'margin-right':'30px','margin-left':'30px'}, className="shadow-lg p-1 mb-5 bg-white rounded"),

    # Indicateurs
    html.Div([
        html.Div(id='total-properties', className="indicator"),
        html.Div(id='average-value', className="indicator"),
    ], style={'margin-right':'30px','margin-left':'30px'}, className="shadow-lg p-1 mb-5 bg-white rounded"),

    html.Div([
        dmc.Grid([
            dmc.Col([
                dcc.Graph(id='property-value-by-commune', className="shadow-lg p-1 mb-5 bg-white rounded"),
            ], span=6),
            
            dmc.Col([
                dcc.Graph(id='property-count-by-local-type', className="shadow-lg p-1 mb-5 bg-white rounded"),
            ], span=6),  
        ]),
    ],style={'margin-right':'30px','margin-left':'30px'}, className="shadow-lg p-1 mb-5 bg-white rounded"),


    html.Hr(),
    html.Br()
    
], fluid=True)])



# Callback pour mettre à jour les éléments du tableau de bord en fonction des filtres
@callback(
    [Output('total-properties', 'children'),
     Output('average-value', 'children'),
     Output('property-value-by-commune', 'figure'),
     Output('property-count-by-local-type', 'figure')],
    [Input('commune-filter', 'value'),
     Input('type-local-filter', 'value')]
)

def update_dashboard(selected_communes, selected_local_types):
    # Filtrer les données en fonction des communes et des types locaux sélectionnés
    filtered_data = data[data['Commune'].isin(selected_communes) & data['Type local'].isin(selected_local_types)]

    # Calculer les indicateurs
    total_properties = len(filtered_data)
    average_value = filtered_data['Valeur fonciere'].mean()

    # Créer un graphique pour la valeur foncière par commune
    property_count_by_Commune = filtered_data.groupby(['Commune'])['Valeur fonciere'].mean()
    fig1 = {
        'data': [
            {'x': property_count_by_Commune.index, 'y': property_count_by_Commune.values, 'name': 'Valeur fonciere', 'type':'bar'}
        ],
        'layout': {
            'title': 'Average land value per municipality',
            'xaxis': {'title': 'Municipality'},
            'yaxis': {'title': 'Land value'}
        }
    }
    
    # Créer un graphique pour le nombre de biens fonciers par type local
    property_count_by_local_type = filtered_data['Type local'].value_counts()
    fig2 = {
        'data': [
            {'x': property_count_by_local_type.index, 'y': property_count_by_local_type.values, 'type': 'bar', 'name': 'Nombre de biens fonciers'}
        ],
        'layout': {
            'title': 'Number of properties by local type',
            'xaxis': {'title': 'Local type'},
            'yaxis': {'title': 'Number of properties'}
        }
    }
    msg_1= dbc.Button([
        "Total number of properties:",
        dbc.Badge(f"{total_properties}", color="light", text_color="primary", className="ms-1"),
    ], color="primary")
    msg_2= dbc.Button([
        "Average land value:",
        dbc.Badge(f"{average_value:.2f}", color="light", text_color="primary", className="ms-1"),
    ], color="primary")
    return msg_1, msg_2, fig1, fig2
