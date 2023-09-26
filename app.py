import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
  html.H1('Sales breakdowns')])


if __name__ == '__main__':
    app.run_server(debug=True)