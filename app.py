# -*- coding: utf-8 -*-
# author: Jorge Gomes for VOST Portugal

# ------------------------------
#      VERSIONS
# ------------------------------

# V 1.0 22 MAR 2022 - The basics

# PROCIV CHECKER

# ------------------------------
#       IMPORT LIBRARIES
# ------------------------------

# ---------- IMPORT BASIC LIBRARIES ------------

import json
import requests
import pandas as pd 
import datetime as dt 
from datetime import datetime, timedelta, date 

# ---------- IMPORT PLOTLY LIBRARIES ------------
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# ---------- IMPORT DASH LIBRARIES ------------
import dash
import dash_daq as daq
from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc


# ------------------------------
#       INITIAL VARIABLES 
# ------------------------------

# Define Start Date to Today
end_date = dt.datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')
# Define Initial button status
selector = 1
# Define Initial Limit 
limit = 100000

# Define Initial URLs
url_bar = f"https://api.fogos.pt/v2/incidents/search" \
f"?before={end_date}" \
f"&after={start_date}" \
f"&limit={limit}" \
f"&all={selector}" \



# ------------------------------
#      GET INITIAL DATA
# ------------------------------

# Get response from URL 
response = requests.get(url_bar)

# Get the json content from the response
json = response.json()


# ------------------------------
#        DATA TREATMENT
# ------------------------------

# Create Pandas Dataframe from the normalized json response
# that begins at "data" level. 
# Depending on your json file this may vary. 
# Use print(json) in order to check the  structure of your json fle
df_in = pd.json_normalize(json,'data')

# Create day column by extracting the day from the date column
df_in['day'] = pd.DatetimeIndex(df_in['date']).day
# Convert seconds to DateTime format 
df_in['dateTime.sec'] = pd.to_datetime(df_in['dateTime.sec'], unit='s')

# Create Dataframes for the first graphs

df_in_pie = df_in.groupby(['natureza','day','familiaName'],as_index=False)['sadoId'].nunique()
df_in_bar = df_in.groupby(['natureza','date'],as_index=False)['sadoId'].nunique()
df_in_line = df_in.groupby(['dateTime.sec'],as_index=False)['sadoId'].nunique()


# ------------------------------
#      DEFINE GRAPHS
# ------------------------------

# Define pie, bar, and line graphs 
fig_pie = px.pie(df_in_pie,names='natureza',values='sadoId',color='natureza',hole=0.5,color_discrete_sequence=px.colors.sequential.Viridis)
fig_bar = px.bar(df_in_bar,x='date',y='sadoId', color='natureza',color_discrete_sequence=px.colors.sequential.Viridis_r,template='plotly_dark')
fig_line = px.line(df_in_line,x='dateTime.sec',y='sadoId', color_discrete_sequence=px.colors.sequential.Viridis_r,template='plotly_dark')

# Styling for graphs

fig_pie.update_traces(textposition='inside', textinfo='value+percent+label')
fig_pie.update_layout(uniformtext_minsize=12, uniformtext_mode='hide',template='plotly_dark')

# ------------------------------
#      START DASH APP
# ------------------------------

app = dash.Dash(
    external_stylesheets=[dbc.themes.CYBORG],
    title='VOSTPT:DASHBOARD',update_title=None,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

# ------------------------------
#      START APP LAYOUT
# ------------------------------
app.layout = dbc.Container(
    [
        # First Row
        dbc.Row(
            [
                # Ttitle Column 
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
                    xs=12, sm=12, md=6, lg=6, xl=6,
                ),
                # SUBTITLE (RIGHT) TITLE COLUMN 
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
                    xs=12, sm=12, md=6, lg=6, xl=6,
                ),
                
            ],
            className="g-0",
        ),  # END OF FIRST ROW 

        # SECOND ROW 
        dbc.Row(
            # HORIZONTAL LINE (NEEDS CSS file in ASSETS FOLDER)
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
                    xs=12, sm=12, md=12, lg=12, xl=12,
                ),
            ),
        # THIRD ROW 
        dbc.Row(
            [
                dbc.Col(
                    # DATE PICKER 
                    dcc.DatePickerRange(
                        id='date-picker',
                        min_date_allowed=date(1995, 8, 5),
                        max_date_allowed=datetime.today(),
                        initial_visible_month=date(2022, 2, 1),
                        display_format='D/M/Y',
                        start_date=date.today(),
                        end_date=date.today()
                    ),
                xs=12, sm=12, md=2, lg=2, xl=2,
                ),
                html.Hr(),
            ],
        ),
                # TOGGLE SWITCH FOR FIRES
        dbc.Row(
            [
                dbc.Col(
                    
                        html.H5("Apenas Incêndios",style={"color":"white"}),
                    
                xs=6, sm=6, md=2, lg=2, xl=2,
                ),
                dbc.Col(
                    daq.ToggleSwitch(
                            id='fire_switch',
                            vertical=False,
                            size=40,
                            value=False,
                            color="#F8D03D",
                            
                            
                        ), 
                    xs=6, sm=6, md=1, lg=1, xl=1,

                    ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                        html.Div(
                            [
                            html.H5("Apenas FMA",style={"color":"white"}),
                            ],
                            ),
                xs=6, sm=6, md=2, lg=2, xl=2,
                ),
                
                dbc.Col(
                    daq.ToggleSwitch(
                            id='fma_switch',
                            vertical=False,
                            size=40,
                            value=False,
                            color="#08519C",
                            
                            
                        ), 
                    xs=6, sm=6, md=1, lg=1, xl=1,

                    ),
                ],
        ),
            
        
        # FOURTH ROW 
        dbc.Row(
            [
                
                        dbc.Col(
                            dcc.Loading(id='loader_pie', 
                                type='dot',
                                color='#FFFFFF',
                                children=[
                                    dcc.Graph(id="graph_pie", figure=fig_pie), # PIE CHART
                                ],
                            ),
                            xs=12, sm=12, md=12, lg=12, xl=12,
                        ),
            ],
        ),
        dbc.Row(
                [
                        dbc.Col(
                            dcc.Loading(id='loader_bar', 
                                type='dot',
                                color='#FFFFFF',
                                children=[
                                    dcc.Graph(id="graph_bar", figure=fig_bar), # BAR CHART
                                    ],
                            ),
                            xs=12, sm=12, md=12, lg=12, xl=12,
                        ), 
                ],
        ),
                    
                
            
        
        
        # FIFTH ROW 
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="graph_line", figure=fig_line),xs=12, sm=12, md=12, lg=12, xl=12) # LINE GRAPH
            ],
            className="g-0",
        ),
    ],
)


# ------------------------------
#      START CALLBACKS
# ------------------------------

# Graphs CallBack 
# Three inputs: two from DatePicker one from Toggle Switch

@app.callback(
    
    Output(component_id="graph_pie",component_property="figure"),
    Output(component_id="graph_bar",component_property="figure"),
    Output(component_id="graph_line",component_property="figure"),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('fire_switch', 'value'),
    Input('fma_switch','value'),

)

# Define what happens when datepicker or toggle switch change

def new_graphs(start_date,end_date,fma_switch,fire_switch):
   
    # Toggle Switch Check 
    # If off selector stays 1 
    # If on selector changes to 0 
    # Yeah, it doesn't make sense. 
    # Should be 0 for all and 1 for specific incidents
    # Complaints? Speak with Tomahock 

    if fire_switch == False and fma_switch == False:
            selector = 1
            fma = 0
            colors = px.colors.sequential.Viridis_r 
            limit = 100000
            url_dash = f"https://api.fogos.pt/v2/incidents/search" \
            f"?before={end_date}" \
            f"&after={start_date}" \
            f"&limit={limit}" \
            f"&fma={fma}" \
            f"&all={selector}" \

    elif fire_switch == True and fma_switch == False:
            selector = 1 
            fma = 1
            colors = px.colors.sequential.Blues
            limit = 100000
            url_dash = f"https://api.fogos.pt/v2/incidents/search" \
            f"?before={end_date}" \
            f"&after={start_date}" \
            f"&limit={limit}" \
            f"&fma={fma}" \
            f"&all={selector}" \

    elif fire_switch == False and fma_switch == True:
            selector = 0
            fma = 0
            colors = px.colors.sequential.Inferno_r
            limit = 100000
            url_dash = f"https://api.fogos.pt/v2/incidents/search" \
            f"?before={end_date}" \
            f"&after={start_date}" \
            f"&limit={limit}" \
            f"&fma={fma}" \
            f"&all={selector}" \

    else:
            selector = 1
            fma = 0
            colors = px.colors.sequential.Viridis_r
            limit = 100000
            url_dash = f"https://api.fogos.pt/v2/incidents/search" \
            f"?before={end_date}" \
            f"&after={start_date}" \
            f"&limit={limit}" \
            f"&fma={fma}" \
            f"&all={selector}" \

    


    # Get response from API CALL 
    response_dash = requests.get(url_dash)
  
    # Get the json content from the response
    json_dash = response_dash.json()
  
    # Create Pandas Dataframe from the normalized json response
    # that begins at "data" level. 
    # Depending on your json file this may vary. 
    # Use print(json) in order to check the  structure of your json fle
    df_dash = pd.json_normalize(json_dash,'data')

    # Create day column by extracting the day from the date column
    df_dash['day'] = pd.DatetimeIndex(df_dash['date']).day.astype(str)
    # Convert seconds to Date Time format 
    df_dash['dateTime.sec'] = pd.to_datetime(df_dash['dateTime.sec'], unit='s')

   
    # -------------------------------------------
    # Create dataframes for the updated graphs 
    # -------------------------------------------

    df_in_pie = df_dash.groupby(['natureza','day','familiaName'],as_index=False)['sadoId'].nunique()
    df_in_bar = df_dash.groupby(['natureza','date'],as_index=False)['sadoId'].nunique()
    df_in_line = df_dash.groupby(['dateTime.sec','natureza'],as_index=False)['sadoId'].nunique()

   

    df_half = df_in_line.resample('15min', on='dateTime.sec', offset='01s').sadoId.count().to_frame().reset_index()


    # ------------------------------
    # DEFINE THE UPDATED GRAPHS
    # ------------------------------


    # Define pie, bar, and line graphs 
    fig_pie = px.pie(df_in_pie,names='natureza',values='sadoId',color='natureza',hole=0.5,color_discrete_sequence=colors)
    fig_bar = px.bar(df_in_bar,x='date',y='sadoId', color='natureza',color_discrete_sequence=colors,template='plotly_dark')
    fig_line = px.line(df_half,x='dateTime.sec',y='sadoId',color_discrete_sequence=colors,template='plotly_dark',labels={"dateTime.sec":"DATA","sadoId":"Ocorrências"})

    # Styling for graphs

    fig_pie.update_traces(textposition='inside', textinfo='value+percent+label')
    fig_pie.update_layout(uniformtext_minsize=12, uniformtext_mode='hide',template='plotly_dark')
    fig_line.update_xaxes(nticks=5)
    fig_bar.update_xaxes(nticks=5)


    # ------------------------------
    #        RETURN CALLBACK
    # ------------------------------


    return fig_pie, fig_bar, fig_line


# ------------------------------
#      RUN DASH APP
# ------------------------------

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug=False, port=8082)



# ------------------------------
#     APP ENDS HERE 
# ------------------------------

# Made with 🤍 by Jorge Gomes MARCH 2022


