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

#app = dash.Dash(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#app = dash.Dash(__name__, external_stylesheets='https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css')

server = app.server
#px.set_mapbox_access_token("pk.eyJ1IjoibWpzcGFubiIsImEiOiJja2ZmaWEwOG8wYzRuMnJwaW1kd2tnNzlkIn0.SoDj7lwJ8uCgC01Is9_IlA")

df = pd.read_csv('./data/updatedschools.csv', index_col=0, parse_dates=True)

ac = df[['School','LATITUDE','LONGITUDE','Bdate', 'Indicator','siz']].copy() 

beginDate = ac['Bdate'].unique()   #numpy ndarray of just the school names

sch = pd.DataFrame()
 
for d in beginDate:
     rowsByDate = ac[ac['Bdate'] == d]       
     #rowsByDate['Bdate'] = pd.to_datetime(rowsByDate.Bdate)    
     sorted = rowsByDate.sort_values(by=['Bdate']).sort_values(by=['Bdate'])   
     j3 = sorted.iloc[[0,-1]] #  looking for the last row wchich indicates the date nearest to  today
     j4 = j3.iloc[[1]]        ## reduce 2 row return to just 1 row again closed to today
     sch = sch.append(j4)
     print(rowsByDate)
"""     
sch['Bdate'] = sch.Bdate.astype(str)
 
schs = sch.sort_values(by=['Bdate'])   

map = px.scatter_mapbox(schs, 
                                lat="LATITUDE", 
                                lon="LONGITUDE",                    
                                color="Indicator", 
                                animation_frame="Bdate",
                                #animation_group="School",
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
    title = "Schools that have been Quarantined",
    titlefont=dict(
            family='sans-serif, monospace',
            size=15,
            color='#090909'
            ),
)


#############################################################################################
app.layout = dbc.Container(
                html.Div([ 
                  dbc.Row([
                      dbc.Col(
                          html.Div(
                              dcc.Graph(
                                  id="Map Graphic5",
                                  figure=map, 
                                  style={'height':'100vh'}
                                 )),
                          )
                        ]),
                   
    ]),fluid = True
)



if __name__ == "__main__":
    app.run_server(host='0.0.0.0')
"""
