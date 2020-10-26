# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
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
#px.set_mapbox_access_token("pk.eyJ1IjoibWpzcGFubiIsImEiOiJja2ZmaWEwOG8wYzRuMnJwaW1kd2tnNzlkIn0.SoDj7lwJ8uCgC01Is9_IlA")

df = pd.read_csv('./data/updatedschools.csv', index_col=0, parse_dates=True)


##########################################################################################

df1 = df[df.QS.notnull()]

sf = df1.groupby('Bdate', as_index=False)['QS'].sum()

sf['Bdate'] = pd.to_datetime(sf.Bdate)

af = sf.sort_values(by=['Bdate'])

fig = px.line(x=af['Bdate'], y=af['QS'])

fig.update_layout(
    title = "Each Day's Quanantine Announcement Totals of Adults and Children, not Accumulative",
    margin=dict(l=20,r=20,t=70,b=40),
    xaxis = dict(title='District opened on Aug 17',titlefont=dict(family='Helvetica, monospace',size=12,color='#7f7f7f')),
    yaxis = dict(title='Quarantine Level',titlefont=dict(family='Helvetica, monospace',size=12,color='#7f7f7f')),
    )
##################################################################################
dfq = pd.read_csv("./data/daily_Q_num.csv")

sfq = dfq.groupby('Bdate', as_index=False)['dailyQ'].mean()

sfq['Bdate'] = pd.to_datetime(sfq.Bdate)

afq = sfq.sort_values(by=['Bdate'])

QL= px.line(x=afq['Bdate'], y=afq['dailyQ'])

QL.update_layout(
    margin=dict(l=20,r=20,t=70,b=40),
    title = "District's Daily Accumulative Quarantine Level with Start and End Dates",
    titlefont=dict(
            family='sans-serif, monospace',
            size=15,
            color='#090909'
            ),
    xaxis = dict(
        title='District opened on Aug 17',
        titlefont=dict(
            family='Helvetica, monospace',
            size=12,
            color='#7f7f7f'
            )
        ),
    yaxis = dict(
        title='Quarantine Level',
        titlefont=dict(
            family='Helvetica, monospace',
            size=12,
            color='#7f7f7f'
            )
        )
    )
   
#########################################################################################
sf1 = df1.groupby('School', as_index=False)['QS'].sum()

names=sf1['School']
values=sf1['QS']

PIE = px.pie(sf1,names=names,values=values)

PIE.update_layout(
    margin=dict(l=0,r=0,t=70,b=40),
    title = "Daily Quarantine Level per School",
    titlefont=dict(
            family='sans-serif, monospace',
            size=15,
            color='#090909'
            ),)


##########################################################################################
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


app.layout = dbc.Container(
                html.Div([
                html.H2('GREELEY PUBLIC SCHOOL DISTRICT 6 Covid-19       By the Numbers'),
                                 html.P('Open Source Independent look at Obfuscated District data'),
                                 html.P(''),                  
                  dbc.Row([
                      dbc.Col(                          
                          html.Div(                             
                              dcc.Graph(
                                  id="Map Graphic1",
                                  figure=fig, 
                                  style={'height':'25vh'})
                              )),
                      dbc.Col(
                          html.Div(
                              dcc.Graph(
                                  id="Map Graphic2",
                                  figure=QL, 
                                  style={'height':'25vh'})
                                )),
                        ]),
                  html.P(),      
                  dbc.Row([
                      dbc.Col(
                          html.Div(
                              dcc.Graph(
                                  id="Map Graphic4",
                                  figure=PIE, 
                                  style={'height':'50vh'})
                              )),
                      dbc.Col(
                          html.Div(
                              
                              dcc.Graph(
                                  id="Map Graphic5",
                                  figure=map, 
                                  style={'height':'50vh'}
                                 )),
                          )
                        ])
    ]),fluid = True
)



if __name__ == "__main__":
    app.run_server(host='0.0.0.0')