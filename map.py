#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 09:02:18 2020

@author: mspann
"""

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


#px.set_mapbox_access_token("pk.eyJ1IjoibWpzcGFubiIsImEiOiJja2ZmaWEwOG8wYzRuMnJwaW1kd2tnNzlkIn0.SoDj7lwJ8uCgC01Is9_IlA")

df = pd.read_csv('./data/updatedschools.csv', index_col=0, parse_dates=True)


map = px.scatter_mapbox(df, 
                                lat="LATITUDE", 
                                lon="LONGITUDE",                    
                                color="Indicator",                               
                                hover_data={'LATITUDE': False,
                                            'LONGITUDE': False,
                                            'siz':False,
                                            'Indicator': False,
                                            'School': True
                                            },
                                color_discrete_map={'Closed': "blue",
                                                    'Quarantined': "red",
                                                    'Clear': "green"},
                                
                                size="siz",
                                zoom=10.5
                                
                                )
map.update_layout(
    mapbox_style="open-street-map",
    mapbox=dict(
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=40.41,
            lon=-104.75
        )
    ),
    margin=dict(l=0,r=50,t=60,b=40),
    title = "Evans Greeley School District 6 - Schools Status by color - October 7th 2020",
    titlefont=dict(
            family='sans-serif, monospace',
            size=15,
            color='#090909'
            ),
    )
    
if __name__ == "__main__":
    app.run_server()