# -*- coding: utf-8 -*-
from ast import Str
from dash import Dash, dcc, html, Input, Output,callback,State,dash_table
import dash_bootstrap_components as dbc
import os,sys,subprocess
import pandas as pd 
import pathlib
import pickle
import logging
#FORMAT = '%(asctime)s %(message)s'
#logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
import joblib





from page_1 import page_1_layout 
from page_2 import page_2_layout
from page_3 import page_3_layout

# navigation bar layout (to switch pages)
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Land value comparison", href="page_1")),
        dbc.NavItem(dbc.NavLink("Land values map", href="page_2")),
        dbc.NavItem(dbc.NavLink("About us", href="page_3")),

    ],
    brand=html.H3("French Land Values",),
    #brand_href="#",
    color="black",
    dark=True,
    style={'height':'100px','font-size':'medium'},
    brand_style={"font-size":"medium"},
    brand_href='/page_1',
    className = "shadow-lg p-3"
)
# app creation (main call)
app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True,
 meta_tags=[{"name": "viewport", "content": "width=device-width"}],

)

app.title = "Land Value Dashboard"
server = app.server


# layout/ UI of the app
url_bar_and_content_div  = html.Div([navbar,
    dcc.Location(id="url", refresh=False), 
    html.Div(id="page-contents")
    #dbc.Button("Take Screenshot", color="dark", className="me-1",id='screenshot-button',style={'position':'relative','left': '47%'})
])
app.layout = url_bar_and_content_div




# Update page
@app.callback([Output("page-contents", "children"),Output("url",'pathname')], [Input("url", "pathname")])
def display_page(pathname):
    """ returns pages depending of the href """
    if pathname == "/page_2":
        return html.Div([page_2_layout]), "/page_2"
    elif pathname == "/page_3": 
        return html.Div([page_3_layout]),"/page_3"
    else: 
        return html.Div([page_1_layout]), "/page_1"



if __name__ == '__main__':
    app.run_server(host="0.0.0.0",debug=True)