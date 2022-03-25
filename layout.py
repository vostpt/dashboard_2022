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
#                  TOP ROW
# -----------------------------------------------

header_row = dbc.Row(
        		[
	        	dbc.Col(

	        		html.Hr(
	        			style={
	        			"borderWidth": "1vh",
	        			"width": "100%",
	        			"borderColor": "#0B4EA2",
	        			"backgroundColor":"#EE1C24",
	        			"background":"#EE1C24",
	        			"opacity": "unset",
	        			}
	        			),
	        		xs=12, sm=12, md=12, lg=12, xl=12,
	        		),
	        	],
        	
    	),  # END OF FIRST ROW 