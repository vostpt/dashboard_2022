# -*- coding: utf-8 -*-
# Original Code by Jorge Gomes for VOST Portugal

# -----------------------------------------------
#                  LIBRARIES
# -----------------------------------------------

# Import Dash and Dash Bootstrap Components
import dash
import dash_daq as daq
from dash import Input, Output, dcc, html, dash_table
import dash_bootstrap_components as dbc


# -----------------------------------------------
#                    LOGOS
# -----------------------------------------------


brand_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],title='CONFIRM - SK4U',update_title=None,
	meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)


VOSTPT_LOGO =  brand_app.get_asset_url('VOSTPT_Logotype.png')
CONFIRM_LOGO = brand_app.get_asset_url('vostportugal_white.png')
PROJECT_LOGO = brand_app.get_asset_url('dashboard_white.png')




logos = dbc.Row(
			[
			dbc.Col(html.Hr(style={"height":"10px","color":"black"}),xs=12, sm=12,md=12,lg=12,xl=12,),
			dbc.Col(html.Img(src=VOSTPT_LOGO, height="50px"),xs=3, sm=3,md=3,lg=2,xl=1,),   	# VOSTPT LOGO - DO NOT REMOVE
			dbc.Col(html.Img(src=PROJECT_LOGO, height="50px"),xs=4, sm=4,md=3,lg=2,xl=2,), 	# PROJECT LOGO
			dbc.Col(xs=1, sm=1,md=3,lg=6,xl=6),
			dbc.Col(html.Img(src=CONFIRM_LOGO, height="50px"),xs=4, sm=4,md=3,lg=2,xl=2,),  # CONFIRM LOGO - DO NOT REMOVE
			

			], 
			className="g-0",
	),  # END OF SECOND ROW 