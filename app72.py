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


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

server = app.server

df = pd.read_csv('./data/updatedschools.csv', index_col=0, parse_dates=True)

ac = df[['School','LATITUDE','LONGITUDE','Bdate', 'Indicator','siz']].copy() 

#dg = df.groupby('Bdate', as_index=False)['School','LATITUDE','LONGITUDE','Bdate','Indicator','siz'].agg()

ac['Bdate'] = pd.to_datetime(ac.Bdate)

sdg = ac.sort_values(by=['Bdate'])

sdg['Bdate'] = sdg['Bdate'].astype(str)

school = df['School'].unique()   #numpy ndarray of just the school names

#######################################################   Animation
map1 = px.scatter_mapbox(sdg, 
                                lat="LATITUDE", 
                                lon="LONGITUDE",                    
                                color="siz", 
                                animation_frame="Bdate",
                                animation_group="Bdate",
                                hover_data={'LATITUDE': False,
                                            'LONGITUDE': False,
                                            'siz':False,
                                            'Indicator': False,
                                            'School': True
                                            },
                                color_discrete_map={'1': "blue",
                                                    '2': "red",
                                                    '3': "green"},
                                size="siz",
                                zoom=11.5                                
                                )


map1.update_layout(
    showlegend=False,
    mapbox_style="open-street-map",
    mapbox=dict(
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=40.41,
            lon=-104.75
        )
    ),
    margin=dict(l=0,r=50,t=60,b=40),
    title = "Schools that have been Quarantined",
    titlefont=dict(
            family='sans-serif, monospace',
            size=15,
            color='#090909'
            ),
)


############################################################  Static Map with markers 
map2 = px.scatter_mapbox(ac, 
                                lat="LATITUDE", 
                                lon="LONGITUDE",                    
                                 hover_data={'LATITUDE': False,
                                            'LONGITUDE': False,
                                            'siz':False,
                                            'Indicator': False,
                                            'School': False,
                                            },
                                zoom=11.5                                
                                )

map2.update_layout(
   mapbox_style="open-street-map",
    mapbox=dict(
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=40.41,
            lon=-104.75
        )
    ),
    margin=dict(l=0,r=50,t=60,b=40),
    title = "Schools that have been Quarantined",
    titlefont=dict(
            family='sans-serif, monospace',
            size=15,
            color='#090909'
            ),
)

map1.add_trace(map2.data[0])
##################################################


###########################################
app.layout = dbc.Container(
                html.Div([ 
                  dbc.Row([
                      dbc.Col(
                          html.Div(
                              dcc.Graph(
                                  id="Map Graphic5",
                                  figure=map1, 
                                  style={'height':'100vh'}
                                 )),
                          )
                        ]),
                   
    ]),fluid = True
)



if __name__ == "__main__":
    app.run_server(host='0.0.0.0')
