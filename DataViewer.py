import dash
import pandas as pd
from datetime import date
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input


# Loading Data from JSON file
df = pd.read_json('data.json')
df = df.rename_axis('date').reset_index()
df = df.iloc[:-2, :]
df['number'] = range(1, len(df)+1)
df['colors'] = "turquoise"
print(df.head()[['date','bpi','number']])
