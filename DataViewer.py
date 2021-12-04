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


# Initailizing the Dah app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY],
               meta_tags=[{'name': 'viewport',
                           'content': 'width=device-width, initial-scale=1.0'}]
               )


# App Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Bitcoin Historic Prices", className='text-center mt-3 mb-3',style={'color':'white'})
        ], width={'size': 10})
    ]),
    
    
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Select Amount:"),
                            dbc.Input(id='d-amount', type='number',
                                      step=1000, value=10000),
                            dcc.Slider(id="slider", min=10000, max=1000000,
                                       step=1000, value=10000,
                                       className="mt-3"),
                        ])
                    ],style={'backgroundColor':' #17202a ','color':'white'})
                ], width=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Select Buy $ Sell Dates:"),
                            dcc.DatePickerSingle(
                                id='my-date-picker-start',
                                min_date_allowed=date(2019, 9, 1),
                                max_date_allowed=date(2021, 9, 5),
                                initial_visible_month=date(2019, 9, 1),
                                date=date(2019, 9, 1),
                                
                            ),
                            dcc.DatePickerSingle(
                                id='my-date-picker-end',
                                min_date_allowed=date(2019, 9, 1),
                                max_date_allowed=date(2021, 9, 5),
                                initial_visible_month=date(2020, 12, 5),
                                date=date(2021, 9, 5),
                                
                            ),
                            dcc.RangeSlider(id="slider-date", min=1,
                                            max=389,
                                            step=1, value=[48, 350],
                                            allowCross=False,
                                            className="mt-3"),

                        ])
                    ],style={'backgroundColor':' #17202a ','color':'white'})
                ], width=6),
            ]),

            dbc.Row(
                dbc.Col(html.Hr(style={'border': "3px solid gray"}),width=12)
            ),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Buy Price"),
                            html.H2(id="bought", children="", style={'fontWeight':'bold'})
                        ])
                    ],style={'backgroundColor':' #17202a ','color':'white'})
                ], width=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Sell Price"),
                            html.H2(id="sold", children="", style={'fontWeight':'bold'})
                        ])
                    ],style={'backgroundColor':' #17202a ','color':'white'})
                ], width=6)
            ], className="mb-3"),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("My Profit"),
                            html.H2(id="profit_num", children="", style={'fontWeight':'bold'})
                        ])
                    ],style={'backgroundColor':' #17202a ','color':'white'})
                ], width=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Profit %"),
                            html.H2(id="profit_pct", children="", style={'fontWeight':'bold'})
                        ])
                    ],style={'backgroundColor':' #17202a ','color':'white'})
                ], width=6)
            ], className="mb-3"),
            
        ], width=4),

        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.P("Bitcoin Price $ and Buy - Sell Price Range by Date"),
                            dcc.Graph(id="bar-chart", config={'displayModeBar': True},
                                      figure=px.bar(df, x='date', y='bpi').
                                      update_layout(margin=dict(l=20, r=20, t=30, b=20))
                                      )
                        ])
                    ],style={'backgroundColor':' #17202a ','color':'white'})
                ], width=12),
            ])
        ], width=7)
    ],className="mt-3", justify='center')
], fluid=True, style={'backgroundColor':'#1c2833'}, className='mb-5')




# Adding Callbacks
# Select Amount 
@app.callback(
    Output('d-amount','value'),
    Output('slider','value'),
    Input('d-amount','value'),
    Input('slider', 'value')
)
def update_purchase_amount(input_v, slider_v):
    ctx = dash.callback_context
    component_triggered = ctx.triggered[0]["prop_id"].split(".")[0]
    if component_triggered == 'slider':
        input_v = slider_v
    else:
        slider_v = input_v

    return input_v, slider_v



# Select Buy and Sell Dates 
@app.callback(
    Output('my-date-picker-start','date'),
    Output('my-date-picker-end','date'),
    Output('slider-date','value'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
    Input('slider-date', 'value'),
)
def update_purchase_amount(start_date, end_date, slider_v):
    ctx = dash.callback_context
    component_triggered = ctx.triggered[0]["prop_id"].split(".")[0]

    if component_triggered == 'slider-date':
        start_date = df[df.number == slider_v[0]]['date'].values[0]
        end_date = df[df.number == slider_v[1]]['date'].values[0]

    elif component_triggered == 'my-date-picker-start' or component_triggered == 'my-date-picker-end':
        num_start = df[df.date==start_date]['number'].values[0]
        num_end = df[df.date==end_date]['number'].values[0]
        slider_v = [num_start, num_end]

    return start_date, end_date, slider_v


# Update Graph
@app.callback(
    Output('bar-chart','figure'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
)
def update_graph(start_date, end_date):
    dff = df.copy()
    dff.loc[((dff.date>=start_date) & (dff.date<=end_date)), 'colors'] = 'black'
    fig = px.bar(dff, x='date', y='bpi',template='plotly_dark')
    fig.update_traces(marker_color=dff['colors'])
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))

    return fig



# Update Price and Profit
@app.callback(
    Output('bought','children'),
    Output('sold','children'),
    Output('profit_num','children'),
    Output('profit_pct', 'children'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
    Input('slider', 'value'),
)
def prices_profit(start_date, end_date, slider_v):
    buy_price = df[df.date == start_date]['bpi'].values[0]
    buy_price_formatted = f"${buy_price:,.2f}"
    sold_price = df[df.date == end_date]['bpi'].values[0]
    sold_price_formatted = f"${sold_price:,.2f}"

    new_v = slider_v / 1000
    my_profit = (sold_price - buy_price) * new_v
    my_profit = f"${my_profit:,.0f}"

    margin = sold_price - buy_price
    my_pct_profit = (margin / buy_price) * 100
    my_pct_profit = f"{my_pct_profit:,.0f}%"

    return buy_price_formatted, sold_price_formatted, my_profit, my_pct_profit



if __name__ == "__main__":
    app.run_server(debug=True, port=8001)