# -*- coding: utf-8 -*-
# author: Jorge Gomes for VOST Portugal

# PROCIV CHECKER

# ________________________________________
# Import Libraries 
import json
import requests
import pandas as pd 
import datetime as dt 
from datetime import datetime, timedelta, date 
# ________________________________________
# Import Plotly Libraries
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
# _________________________________________
# Import Dash and Dash Bootstrap Components
import dash
from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc
# _________________________________________
# INITIAL VARIABLES

# Define Start Date to Today
end_date = dt.datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=4)).strftime('%Y-%m-%d')
# Define Initial button status 
selector = 1

# Define Initial URLs
url_bar = f"https://api.fogos.pt/v2/incidents/search" \
f"?before={end_date}" \
f"&after={start_date}" \
f"&all={selector}" \

# https://api.fogos.pt/v2/incidents/search?before=2022-02-02&after=2022-02-09&all=1

url_pie = f"https://api.fogos.pt/v2/incidents/search" \
f"?after={start_date}" \
f"&all={selector}" \

# _________________________________________
# GET FIRST JSON DATA and DATA Treatment 

# Get response from URL 
response_bar = requests.get(url_bar)
response_pie = requests.get(url_pie)
# Get the json content from the response
json_bar = response_bar.json()
json_pie = response_pie.json()
# Create Pandas Dataframe from the normalized json response
# that begins at "data" level. 
# Depending on your json file this may vary. 
# Use print(json) in order to check the  structure of your json fle
df_json_bar = pd.json_normalize(json_bar,'data')
df_json_pie = pd.json_normalize(json_pie,'data')

df_json_bar['day'] = pd.DatetimeIndex(df_json_bar['date']).day

# print(df_json_bar.info())

# Define dataframes for firsts graphs
# Dataframe will get data by nature of the incident, 
# the hour that is has occurred, 
# and then count the unique values of the unique sadoId column
# This will return the amount of entries for each type of incident
df_bar = df_json_bar.groupby(['natureza','day','familiaName'],as_index=False)['sadoId'].count()
df_pie = df_json_bar.groupby(['natureza'],as_index=False)['sadoId'].count()
df_line = df_json_bar.groupby(['hour'],as_index=False)['sadoId'].count()
# Create a new column for day 

# _________________________________________
# DEFINE THE THREE INITIAL GRAPHS 

# Define pie, bar, and line graphs 
fig_pie = px.pie(df_pie,names='natureza',values='sadoId',color='natureza',hole=0.5,color_discrete_sequence=px.colors.sequential.Viridis)
fig_bar = px.bar(df_bar,x='day',y='sadoId', color='natureza',color_discrete_sequence=px.colors.sequential.Viridis_r,template='plotly_dark')
fig_line = px.line(df_line,x='hour',y='sadoId', color_discrete_sequence=px.colors.sequential.Viridis_r,template='plotly_dark')

# Styling for graphs

fig_pie.update_traces(textposition='inside', textinfo='value+percent+label')
fig_pie.update_layout(uniformtext_minsize=12, uniformtext_mode='hide',template='plotly_dark')



app = dash.Dash(
    external_stylesheets=[dbc.themes.CYBORG],
    #suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.layout = dbc.Container(
    [
        # First Row
        dbc.Row(
            [
                dbc.Col(
                    html.H4("VOST PORTUGAL",
                        style={
                            "borderWidth": "1vh",
                            "width": "100%",
                            "background-color":"#353535",
                            "borderColor": "#353535",
                            "opacity": "unset",
                        }
                    ),
                    width={"size": 6},
                ),
                dbc.Col(
                    html.H4("Dashboard Operacional",
                        style={
                            "borderWidth": "1vh",
                            "width": "100%",
                            "background-color":"#BDBBB0",
                            "text-align":"right",
                            "borderColor": "#BDBBB0",
                            "opacity": "unset",
                        }
                    ),
                    width={"size": 6},
                ),
                
            ],
            className="g-0",
        ),  # end of first row


        dbc.Row(
            dbc.Col(
                    html.Hr(
                        style={
                            "borderWidth": "2vh",
                            "width": "100%",
                            "background-color":"#353535",
                            "borderColor": "#CDE6F5",
                            "opacity": "unset",
                        }
                    ),
                    width={"size": 12},
                ),
            ),
        dbc.Row(
            dbc.Col(
                dcc.DatePickerRange(
                    id='date-picker',
                    min_date_allowed=date(1995, 8, 5),
                    max_date_allowed=datetime.today(),
                    initial_visible_month=date(2022, 2, 1),
                    display_format='D/M/Y',
                    start_date=date.today(),
                    end_date=date.today()
                ),
            width={"size": 6},
            ),
        ),

        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="graph_pie", figure=fig_pie),width={"size": 6}),
                dbc.Col(dcc.Graph(id="graph_bar", figure=fig_bar),width={"size": 6})
            
            ],
            className="g-0",
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="graph_line", figure=fig_line),width={"size": 12})
            ],
            className="g-0",
        ),
    ],
)
@app.callback(
    
    Output(component_id="graph_pie",component_property="figure"),
    Output(component_id="graph_bar",component_property="figure"),
    Output(component_id="graph_line",component_property="figure"),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')

)
def new_graphs(start_date,end_date):

    print("LOOP STARTS HERE")
    print(start_date)
    print(end_date)
    print("---------------------")
   


    selector = 1
    limit = 100000
    url_bar = f"https://api.fogos.pt/v2/incidents/search" \
    f"?before={end_date}" \
    f"&after={start_date}" \
    f"&limit={limit}" \
    f"&all={selector}" \

    url_pie = f"https://api.fogos.pt/v2/incidents/search" \
    f"?after={end_date}" \
    f"&all={selector}" \


    print("URL BAR: "+url_bar)
    print("URL PIE: "+url_pie)

    # Get response from URL 
    response_bar = requests.get(url_bar)
    response_pie = requests.get(url_pie)
    # Get the json content from the response
    json_bar = response_bar.json()
    json_pie = response_pie.json()


    #print("JSON BAR RESULT")
    #print(json_bar)

  

    # Create Pandas Dataframe from the normalized json response
    # that begins at "data" level. 
    # Depending on your json file this may vary. 
    # Use print(json) in order to check the  structure of your json fle
    df_json_bar = pd.json_normalize(json_bar,'data')
    df_json_pie = pd.json_normalize(json_pie,'data')

    print(df_json_bar.head())

    df_json_pie['day'] = pd.DatetimeIndex(df_json_pie['date']).day


    df_bar = df_json_bar.groupby(['natureza','date','familiaName'],as_index=False)['sadoId'].count()
    df_pie = df_json_bar.groupby(['natureza'],as_index=False)['sadoId'].count()
    df_line = df_json_bar.groupby(['date'],as_index=False)['sadoId'].count()

    fig_pie = px.pie(df_pie,names='natureza',values='sadoId',color='natureza',hole=0.5,color_discrete_sequence=px.colors.sequential.Viridis_r)
    fig_bar = px.bar(df_bar,x='date',y='sadoId', color='natureza',color_discrete_sequence=px.colors.sequential.Viridis_r,template='plotly_dark')
    fig_line = px.line(df_line,x='date',y='sadoId', color_discrete_sequence=px.colors.sequential.Viridis_r,template='plotly_dark')

    # Styling for graphs

    fig_pie.update_traces(textposition='inside', textinfo='value+percent+label')
    fig_pie.update_layout(uniformtext_minsize=12, uniformtext_mode='hide',template='plotly_dark')

    return fig_pie, fig_bar, fig_line







# Load APP 

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)


# APP ENDS HERE 


