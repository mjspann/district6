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


##########################################################################################

df1 = df[df.QS.notnull()]

sf = df1.groupby('Bdate', as_index=False)['QS'].sum()

sf['Bdate'] = pd.to_datetime(sf.Bdate)

af = sf.sort_values(by=['Bdate'])

fig = px.line(x=af['Bdate'], y=af['QS'])

fig.update_layout(
    margin=dict(l=20,r=20,t=70,b=40),   
    title = "Each Day's Quanantine Announcement Totals of Adults and Students, not Accumulative",
    titlefont=dict(
            family='Helvetica, monospace',
            size=12,
            color='#090909'
            ),
    xaxis = dict(
            title='District opened on Aug 17',
            titlefont=dict(
                    family='Helvetica, monospace',
                    size=12,
                    color='#7f7f7f')
                    ),
    yaxis = dict(
            title='Quarantine Level',
            titlefont=dict(
                    family='sans-serif, monospace',
                    size=12,
                    color='#7f7f7f')),
    )
##################################################################################
dfq = pd.read_csv("./data/daily_Q_num.csv")

sfq = dfq.groupby('Bdate', as_index=False)['dailyQ'].mean()

sfq['Bdate'] = pd.to_datetime(sfq.Bdate)

afq = sfq.sort_values(by=['Bdate'])

QL= px.line(x=afq['Bdate'], y=afq['dailyQ'])

QL.update_layout(
    margin=dict(l=20,r=20,t=70,b=40),
    title = "District's Daily Accumulative Level utilizing Quarantine Begin and End Dates",
    titlefont=dict(
            family='Helvetica, monospace',
            size=12,
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
sf1 = df1.groupby('School', as_index=False)['QT'].sum()

names=sf1['School']
values=sf1['QT']

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
     
sch['Bdate'] = sch.Bdate.astype(str)
    

map = px.scatter_mapbox(sch, 
                                lat="LATITUDE", 
                                lon="LONGITUDE",                    
                                color="Indicator", 
                                animation_frame="Bdate",
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
                html.H1(''),
                  dbc.Row([
                      dbc.Col(                          
                          html.Div([
                                  html.H1(''),
                                  html.H1('GREELEY PUBLIC SCHOOL DISTRICT 6 Covid-19 unauthorized dashboard'),
                                  html.P('Open Source Independent look at published District covid data'),
                                  html.P('Data is copied from the districts website daily and subject to human error'),
                              
                              ])),
                      dbc.Col(
                              html.Div([
                                  html.H1(''),
                                  html.H1('November 16, 2020'),
                                  html.P(''),
                                  html.P('The School District has 22,000 students, with 1672 quarintined at least once or 7% of the population'),
                                  html.P('The School District has 27 distict operated schools and 6 Charter School for a total of 33 plus the District Office'),
                                  html.P('All but 2 schools have been Quarantined or closed or 88% have been quarantined'),
                                  ]
                                )),
                        ]),
                    html.P(),    
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
                  dbc.Row([
                      dbc.Col(                          
                          html.Div([
                                 
                                  html.P('The Line Graph above shows the frequency of covid activity daily within the District'),
                                  html.P("The graph's x axis is the Begin Date and the y axis is the district population number affected"),
                                
                              
                              ])),
                      dbc.Col(
                              html.Div([
                                  
                                  html.P("The line Graph above illustrates growth of the infection withiin the District's Community"),
                                  
                                  ]
                                )),
                        ]),
                 html.P(),      
                  dbc.Row([
                      dbc.Col(
                          html.Div(
                              
                              dcc.Graph(
                                  id="Map Graphic5",
                                  figure=map, 
                                  style={'height':'50vh'}
                                 )),
                          )
                        ]),
                   
    ]),fluid = True
)



if __name__ == "__main__":
    app.run_server(host='0.0.0.0')

