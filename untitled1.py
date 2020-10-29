#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:38:25 2020

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

server = app.server

df = pd.read_csv('./data/updatedschools.csv', parse_dates=True)

ac = df[['School','LATITUDE','LONGITUDE','Bdate', 'Indicator','siz']].copy() 

schools = ac['School'].unique()   #numpy ndarray of just the school names

sch = pd.DataFrame()
 
for x in schools:
     oneschoolsrows = ac[ac['School'] == x]       
     oneschoolsrows['Bdate'] = pd.to_datetime(oneschoolsrows.Bdate)    
     sorted = oneschoolsrows.sort_values(by=['Bdate']).sort_values(by=['Bdate'])   
     j3 = sorted.iloc[[0,-1]] #  looking for the last row wchich indicates the date nearest to  today
     j4 = j3.iloc[[1]]        ## reduce 2 row return to just 1 row again closed to today
     sch = sch.append(j4)
    

map = px.scatter_mapbox(sch, 
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

app.layout = dbc.Container(
                html.Div([
                html.H2('GREELEY PUBLIC SCHOOL DISTRICT 6 Covid-19'),
                                 html.P('Open Source Independent look at published District covid data'),
                                 html.P('Data is copied from the districts website daily and subject to some human error'),                  
                  dbc.Row([
                      dbc.Col(
                          html.Div(
                              dcc.Graph(
                                  id="Map Graphic4",
                                  figure=map, 
                                  style={'height':'50vh'})
                              )),
                        ])
    ]),fluid = True
)
     
if __name__ == "__main__":
    app.run_server(host='0.0.0.0')