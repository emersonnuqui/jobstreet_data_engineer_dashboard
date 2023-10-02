import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc 
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# Set the background color for the entire HTML body
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body style="background-color: #004AAD;">
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Define custom CSS to import the font
custom_css = [
    html.Link(
        rel="stylesheet",
        href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;500;600;700;800&display=swap"
    )
]

app.layout = html.Div([
    html.Div([html.H1('JOBSTREET DATA ENGINEER DASHBOARD', 
                      style={'font-family': 'Open Sans, sans-serif', 'font-weight': '800', 'text-align': 'center', 'font-size': '63px', 'color':'white'})]),

    html.Div([html.P("Data Engineering has been emerging throughout this year as ", 
                     style={'font-family': 'Open Sans, sans-serif', 'font-weight': '300', 'text-align': 'center', 'color':'white'})]),
    html.P("""Data Engineering has been emerging throughout this year as """, 
           style={'font-family': 'Open Sans, sans-serif', 'font-weight': '300', 'text-align': 'center', 'color':'white'}),


    html.Div(
        children=[
            html.Div(
                dbc.Card(
                    dbc.CardBody([
                        html.H1("Number of Jobs", className="card-title", 
                                style={'font-family': 'Open Sans, sans-serif', 'font-weight': '500', 'text-align': 'center', 'font-size': '20px', 'color':'#000000', 'margin-top':'20px'}),

                        html.P("This is some text within the card.", className="card-text",  style={'font-family': 'Open Sans, sans-serif', 'font-weight': '800', 'text-align': 'center', 'font-size':'24px', 'color':'#000000'}),
                    ], style={'margin-top':'20px'}), style={'background-color': '#00BF63',  'margin':'50px'}),
                style={'width': '20%', 'position': 'relative', 'display': 'inline-block'}
            ),

            html.Div(
                "Column 2",
                style={'width': '40%', 'display': 'inline-block'}
            ),
            html.Div(
                "Column 3",
                style={'width': '40%', 'display': 'inline-block'}
            ),
    ])
  ])


if __name__ == '__main__':
    app.run_server(debug=True)